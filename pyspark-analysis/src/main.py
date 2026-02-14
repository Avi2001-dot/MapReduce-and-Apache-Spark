import os
from pathlib import Path

import findspark

findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql import functions as f


def to_file_uri(p: Path) -> str:
    return "file:///" + str(p.resolve()).replace("\\", "/")


if __name__ == "__main__":
    os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")

    spark = (
        SparkSession.builder
        .master("local[*]")
        .appName("PySparkAssignment1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.python.worker.reuse", "false")
        .getOrCreate()
    )

    project_dir = Path(__file__).parent
    data_glob = project_dir / "data" / "*.txt"
    input_path = to_file_uri(data_glob)

    raw = spark.sparkContext.wholeTextFiles(input_path)

    # Solution 10
    print("\n================ Solution 10 ================\n")

    books_df = (
        raw.toDF(["path", "text"])
        .withColumn("file_name", f.regexp_extract("path", r"([^/\\\\]+)$", 1))
        .select("file_name", "text")
    )

    title_re = r"(?mi)^Title:\s*(.+?)\s*$"
    lang_re = r"(?mi)^Language:\s*(.+?)\s*$"
    enc_re  = r"(?mi)^Character set encoding:\s*(.+?)\s*$"

    release_year_re = r"(?mi)^Release Date:\s*.*?(\b(18|19|20)\d{2}\b)"

    meta = (
        books_df
        .withColumn("title_raw", f.regexp_extract("text", title_re, 1))
        .withColumn("language_raw", f.regexp_extract("text", lang_re, 1))
        .withColumn("encoding_raw", f.regexp_extract("text", enc_re, 1))
        .withColumn("release_year_str", f.regexp_extract("text", release_year_re, 1))
    )

    meta = (
        meta
        .withColumn("title", f.nullif(f.trim(f.col("title_raw")), f.lit("")))
        .withColumn("language", f.nullif(f.trim(f.col("language_raw")), f.lit("")))
        .withColumn("encoding", f.nullif(f.trim(f.col("encoding_raw")), f.lit("")))
        .drop("title_raw", "language_raw", "encoding_raw")
    )

    meta2 = meta.withColumn("release_year", f.expr("try_cast(release_year_str as int)")).drop("release_year_str")

    meta2 = meta2.filter((f.col("release_year").isNotNull()) & (f.col("release_year") >= 1500) & (f.col("release_year") <= 2026))

    books_per_year = meta2.groupBy("release_year").count().orderBy("release_year")

    common_lang = (
        meta2.filter(f.col("language").isNotNull())
        .groupBy("language")
        .count()
        .orderBy(f.desc("count"), f.asc("language"))
    )

    avg_title_len = (
        meta2.filter(f.col("title").isNotNull())
        .select(f.avg(f.length("title")).alias("avg_title_length"))
    )

    print("\n=== Books per year ===")
    books_per_year.show(50, truncate=False)

    print("\n=== Most common languages ===")
    common_lang.show(50, truncate=False)

    print("\n=== Average title length ===")
    avg_title_len.show(truncate=False)

    total_files = books_df.count()
    total_meta = meta.count()
    total_meta2 = meta2.count()


    print(f"Total files read: {total_files}")
    print(f"Rows in meta (before year filter): {total_meta}")
    print(f"Rows in meta2 (after year filter): {total_meta2}")

    missing_year = meta.filter(f.regexp_extract("text", release_year_re, 1) == "")
    missing_cnt = missing_year.count()
    print(f"Rows missing release year: {missing_cnt}")

    if missing_cnt > 0:
        print("\nSample rows missing release year (file_name + first 300 chars):")
        missing_year.select("file_name", f.substring("text", 1, 300).alias("text_head")).show(5, truncate=False)

    # Solution 11
    print("\n================ Solution 11 ================\n")

    from pyspark.ml.feature import RegexTokenizer, StopWordsRemover

    # Remove Gutenberg header/footer (robust)
    cleaned = books_df.withColumn(
        "text_clean",
        f.regexp_replace(
            "text",
            r"(?s)\*\*\* START OF.*?\*\*\* END OF.*?\*\*\*",
            ""
        )
    )

    # Lowercase + remove punctuation
    cleaned = cleaned.withColumn(
        "text_clean",
        f.lower(f.regexp_replace("text_clean", r"[^a-z\s]", " "))
    )

    # Tokenize
    tokenizer = RegexTokenizer(
        inputCol="text_clean",
        outputCol="tokens",
        pattern="\\s+"
    )
    tokenized = tokenizer.transform(cleaned)

    # Remove stopwords
    remover = StopWordsRemover(
        inputCol="tokens",
        outputCol="words"
    )
    processed = remover.transform(tokenized).select("file_name", "words")

    exploded = processed.select(
        "file_name",
        f.explode("words").alias("word")
    )

    tf = (
        exploded.groupBy("file_name", "word")
        .count()
        .withColumnRenamed("count", "term_freq")
    )

    doc_count = books_df.select("file_name").distinct().count()

    df = (
        exploded.select("file_name", "word")
        .distinct()
        .groupBy("word")
        .count()
        .withColumnRenamed("count", "doc_freq")
    )

    idf = df.withColumn(
        "idf",
        f.log(f.lit(doc_count) / f.col("doc_freq"))
    )


    tfidf = (
        tf.join(idf, "word")
        .withColumn("tfidf", f.col("term_freq") * f.col("idf"))
        .select("file_name", "word", "tfidf")
    )
    

    # Compute vector magnitude per book
    magnitudes = (
        tfidf.groupBy("file_name")
        .agg(f.sqrt(f.sum(f.col("tfidf") ** 2)).alias("norm"))
    )

    # Self join to compute dot product
    pairs = (
        tfidf.alias("a")
        .join(tfidf.alias("b"), "word")
        .filter(f.col("a.file_name") < f.col("b.file_name"))
        .select(
            f.col("a.file_name").alias("book1"),
            f.col("b.file_name").alias("book2"),
            (f.col("a.tfidf") * f.col("b.tfidf")).alias("product")
        )
    )

    dot_products = (
        pairs.groupBy("book1", "book2")
        .agg(f.sum("product").alias("dot_product"))
    )

    mag1 = magnitudes.withColumnRenamed("file_name", "book1") \
        .withColumnRenamed("norm", "norm1")
    mag2 = magnitudes.withColumnRenamed("file_name", "book2") \
        .withColumnRenamed("norm", "norm2")

    similarity = (
        dot_products
        .join(mag1, "book1")
        .join(mag2, "book2")
        .withColumn(
            "cosine_similarity",
            f.col("dot_product") / (f.col("norm1") * f.col("norm2"))
        )
        .select("book1", "book2", "cosine_similarity")
    )

    
    # TOP 5 SIMILAR BOOKS TO 10.txt

    target_book = "10.txt"

    top5 = (
        similarity
        .filter(
            (f.col("book1") == target_book) |
            (f.col("book2") == target_book)
        )
        .orderBy(f.desc("cosine_similarity"))
        .limit(5)
    )

    print(f"\n=== Top 5 Similar Books to {target_book} ===")
    top5.show(truncate=False)

    print("\n================ Solution 12 ================\n")

    X = 5


    author_re = r"(?mi)^Author:\s*(.+?)\s*$"


    authors = (
        meta2
        .withColumn("author_raw", f.regexp_extract("text", author_re, 1))
        .withColumn("author", f.nullif(f.trim(f.col("author_raw")), f.lit("")))
        .drop("author_raw")
        .filter(f.col("author").isNotNull())
        .select("file_name", "author", "release_year")
    )

    print("\n=== Sample extracted (file_name, author, release_year) ===")
    authors.show(10, truncate=False)

    a = authors.alias("a")
    b = authors.alias("b")
    edges = (
        a.join(
            b,
            on=(
                    (f.col("a.author") != f.col("b.author")) &
                    (f.col("b.release_year") >= f.col("a.release_year")) &
                    (f.col("b.release_year") <= f.col("a.release_year") + f.lit(X))
            ),
            how="inner"
        )
        .select(
            f.col("a.author").alias("author1"),
            f.col("b.author").alias("author2"),
            f.col("a.release_year").alias("year1"),
            f.col("b.release_year").alias("year2"),
            f.col("a.file_name").alias("book1"),
            f.col("b.file_name").alias("book2"),
        )
    )

    edge_list = edges.select("author1", "author2").distinct()

    print(f"\n=== Edge list sample (author1 -> author2), X={X} years ===")
    edge_list.show(20, truncate=False)

    # out-degree: how many distinct authors this author potentially influenced
    out_degree = (
        edge_list.groupBy("author1")
        .agg(f.countDistinct("author2").alias("out_degree"))
        .withColumnRenamed("author1", "author")
    )

    # in-degree: how many distinct authors potentially influenced this author
    in_degree = (
        edge_list.groupBy("author2")
        .agg(f.countDistinct("author1").alias("in_degree"))
        .withColumnRenamed("author2", "author")
    )

    # Combine degrees (full outer so we keep authors that appear only on one side)
    degrees = (
        out_degree.join(in_degree, on="author", how="full_outer")
        .na.fill(0, subset=["out_degree", "in_degree"])
    )

    print("\n=== Top 5 authors by IN-degree (most influenced) ===")
    degrees.orderBy(f.desc("in_degree"), f.desc("out_degree"), f.asc("author")).show(5, truncate=False)

    print("\n=== Top 5 authors by OUT-degree (most influential) ===")
    degrees.orderBy(f.desc("out_degree"), f.desc("in_degree"), f.asc("author")).show(5, truncate=False)

    print("Total (author,book) rows:", authors.count())
    print("Total distinct edges (author->author):", edge_list.count())

    spark.stop()