from pyspark.sql import SparkSession
from pyspark.sql.functions import *
# use this after opening port with nc -lk 9999

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("Streaming Word Count") \
        .master("local[3]") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .config("spark.sql.shuffle.partitions", 3) \
        .getOrCreate()

    # READ
    lines_df = spark.readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", "9999") \
        .load()

    # TRANSFORM
    words_df = lines_df.select(expr("explode(split(replace(replace(value, ',', ''), '.', ''),' ')) as word"))
    # counts_df = words_df.groupBy("word").count() # the original
    words_df.createOrReplaceTempView("words") # the sql method
    counts_df = spark.sql("select word, count(*) from words group by word")

    # SINK
    word_count_query = counts_df.writeStream \
        .format("console") \
        .outputMode("complete") \
        .option("checkpointLocation", "chk-point-dir") \
        .start()

    print("Listening to localhost:9999")
    word_count_query.awaitTermination()