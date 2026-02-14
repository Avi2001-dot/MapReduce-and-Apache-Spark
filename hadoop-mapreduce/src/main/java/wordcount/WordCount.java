package wordcount;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCount {

    public static class TokenizerMapper 
            extends Mapper<LongWritable, Text, Text, IntWritable> {
        
        // Reusable IntWritable with value 1 for efficiency
        private final static IntWritable one = new IntWritable(1);
        // Reusable Text object for word output
        private Text word = new Text();

        @Override
        public void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {
            
            // Get line as string
            String line = value.toString();
            
            // Handle empty lines gracefully
            if (line == null || line.trim().isEmpty()) {
                return;
            }
            
            // Remove punctuation: replace non-alphabetic characters (except spaces) with empty string
            String cleanLine = line.replaceAll("[^a-zA-Z\\s]", "");
            
            // Tokenize using StringTokenizer (splits on whitespace by default)
            StringTokenizer tokenizer = new StringTokenizer(cleanLine);
            
            // Emit (word, 1) for each token
            while (tokenizer.hasMoreTokens()) {
                String token = tokenizer.nextToken();
                // Skip empty tokens
                if (!token.isEmpty()) {
                    word.set(token);
                    context.write(word, one);
                }
            }
        }
    }

    public static class IntSumReducer 
            extends Reducer<Text, IntWritable, Text, IntWritable> {
        
        // Reusable IntWritable for result
        private IntWritable result = new IntWritable();
        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context)
                throws IOException, InterruptedException {
            
            // Sum all values
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            
            // Set result and emit (word, total_count)
            result.set(sum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        
        // Validate arguments
        if (args.length < 2) {
            System.err.println("Usage: WordCount <input_path> <output_path> [split_size_mb]");
            System.exit(1);
        }
        
        // Create configuration
        Configuration conf = new Configuration();
 
        if (args.length >= 3) {
            long splitSizeMB = Long.parseLong(args[2]);
            long splitSizeBytes = splitSizeMB * 1024 * 1024;
            conf.setLong("mapreduce.input.fileinputformat.split.maxsize", splitSizeBytes);
            System.out.println("Split size set to: " + splitSizeMB + " MB (" + splitSizeBytes + " bytes)");
        }
        
        // Create job
        Job job = Job.getInstance(conf, "WordCount");
        job.setJarByClass(WordCount.class);
        
        // Set Mapper and Reducer classes
        job.setMapperClass(TokenizerMapper.class);
        job.setReducerClass(IntSumReducer.class);
        
        // Set Combiner (optional optimization - same as reducer for WordCount)
        job.setCombinerClass(IntSumReducer.class);
        
        // Set output key and value classes (Problem 4)
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        
        // Set input and output paths
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        
        // Problem 9: Measure and display execution time
        System.out.println("Starting WordCount job...");
        long startTime = System.currentTimeMillis();
        
        // Run job and wait for completion
        boolean success = job.waitForCompletion(true);
        
        long endTime = System.currentTimeMillis();
        long executionTime = endTime - startTime;
        
        // Exit with appropriate code
        System.exit(success ? 0 : 1);
    }
}
