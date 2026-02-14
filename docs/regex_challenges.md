# Regex Challenges and Metadata Issues
## CSL7110 Big Data Frameworks Assignment - Problem 10

## Regular Expressions Used

### Title Extraction
```python
TITLE_PATTERN = r'Title:\s*(.+?)(?:\r?\n|$)'
```
- Matches "Title:" followed by any characters until newline
- `\s*` handles variable whitespace after colon
- `(.+?)` captures title text (non-greedy)
- `(?:\r?\n|$)` handles different line endings

### Release Date Extraction
```python
RELEASE_DATE_PATTERN = r'(?:Release Date|Posting Date):\s*(.+?)(?:\r?\n|$)'
```
- Handles both "Release Date:" and "Posting Date:" variations
- Captures date in various formats (e.g., "January 1, 2000", "2000-01-01")

### Language Extraction
```python
LANGUAGE_PATTERN = r'Language:\s*(.+?)(?:\r?\n|$)'
```
- Simple pattern for "Language: English" format

### Encoding Extraction
```python
ENCODING_PATTERN = r'Character set encoding:\s*(.+?)(?:\r?\n|$)'
```
- Matches the full "Character set encoding:" label

### Author Extraction
```python
AUTHOR_PATTERN = r'Author:\s*(.+?)(?:\r?\n|$)'
```
- Captures author name(s) after "Author:" label

---

## Challenges Encountered

### 1. Format Variations

**Problem**: Different books use different header formats.

```
Book A:
Title: Pride and Prejudice
Author: Jane Austen

Book B:
Title:  Pride and Prejudice   (extra spaces)
Author: Austen, Jane          (different name format)

Book C:
TITLE: PRIDE AND PREJUDICE    (different case)
```

**Solution**: Use case-insensitive matching and flexible whitespace handling:
```python
re.search(pattern, text, re.IGNORECASE)
```

### 2. Multi-line Values

**Problem**: Some titles or descriptions span multiple lines.

```
Title: The Complete Works of William Shakespeare
       Including All Plays and Sonnets
```

**Solution**: Current pattern captures only first line. For complete capture:
```python
TITLE_PATTERN_MULTILINE = r'Title:\s*(.+?)(?=\n[A-Z][a-z]+:|$)'
```

### 3. Missing Fields

**Problem**: Not all books have all metadata fields.

```
Book without language field:
Title: Some Book
Author: Unknown
Release Date: 2000
(no Language field)
```

**Solution**: Return None for missing fields and handle gracefully:
```python
def safe_extract(pattern, text):
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None
```

### 4. Date Format Variations

**Problem**: Dates appear in many formats.

```
Release Date: January 1, 2000
Release Date: 2000-01-01
Release Date: 01/01/2000
Release Date: 1 Jan 2000
Posting Date: January, 2000
```

**Solution**: Extract raw date string, then parse year separately:
```python
YEAR_PATTERN = r'\b(\d{4})\b'
```

### 5. Special Characters

**Problem**: Titles may contain special characters that interfere with regex.

```
Title: What's in a Name? (A Study)
Title: "Quotes" and [Brackets]
```

**Solution**: Use non-greedy matching and proper escaping.

---

## Metadata Quality Issues

### 1. Inconsistent Formatting

| Issue | Example | Frequency |
|-------|---------|-----------|
| Extra whitespace | "Title:  Book Name  " | Common |
| Different cases | "TITLE:", "title:", "Title:" | Occasional |
| Typos | "Tilte:", "Auther:" | Rare |

### 2. Missing Values

| Field | Estimated Missing Rate |
|-------|----------------------|
| Title | ~5% |
| Author | ~15% |
| Release Date | ~10% |
| Language | ~20% |
| Encoding | ~30% |

### 3. Incorrect Values

- Author field contains editor name instead
- Release date is digitization date, not original publication
- Language field contains multiple languages

---

## Handling Strategies for Real-World Scenarios

### 1. Data Validation
```python
def validate_metadata(metadata):
    issues = []
    
    if not metadata.get('title'):
        issues.append('Missing title')
    
    if metadata.get('release_year'):
        year = metadata['release_year']
        if year < 1000 or year > 2100:
            issues.append(f'Invalid year: {year}')
    
    return issues
```

### 2. Fallback Extraction
```python
def extract_title(text):
    # Try primary pattern
    match = re.search(TITLE_PATTERN, text)
    if match:
        return match.group(1).strip()
    
    # Fallback: Look for title in first few lines
    lines = text.split('\n')[:10]
    for line in lines:
        if line.strip() and not line.startswith('*'):
            return line.strip()
    
    return None
```

### 3. Data Cleaning Pipeline
```python
def clean_metadata(df):
    return df \
        .withColumn('title', trim(col('title'))) \
        .withColumn('author', trim(col('author'))) \
        .withColumn('language', 
            when(col('language').isNull(), 'Unknown')
            .otherwise(col('language'))) \
        .filter(col('title').isNotNull())
```

### 4. Logging and Monitoring
```python
def extract_with_logging(text, file_name):
    metadata = extract_all(text)
    
    missing_fields = [f for f in ['title', 'author', 'language'] 
                      if not metadata.get(f)]
    
    if missing_fields:
        logging.warning(f"{file_name}: Missing fields: {missing_fields}")
    
    return metadata
```

---

## Recommendations

1. **Use multiple patterns**: Have fallback patterns for common variations
2. **Validate extracted data**: Check for reasonable values
3. **Log extraction failures**: Track which books have issues
4. **Consider ML approaches**: For complex cases, use NER or text classification
5. **Manual review**: Sample and review extracted data periodically
