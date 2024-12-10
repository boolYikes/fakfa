## Memo
### Kafka
- broker list
- topic list
- acl for each topic
### modes: distribution coordination services
- zookeeper mode
- kraft mode
### partition & replication
- broker < Topics < partitions < segments -> actual log files
### kafka connect
- data brokerage bw db systems
### Docker compose
- many versions exist
- conduktor: a cli
## Exercise
### Issues
- vendor.six.moves error: Use python 3.11 or use kafka-python-ng and
```python
import six
import sys
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves
```
### d
- kafka1 is the broker
- webui is on 8080

|Feature|JSON|Avro|Parquet|
|---|---|---|---|
|Encoding|Text-based|Binary|Binary (columnar)|
|Readability|Human-readable|Not readable|Not readable|
|File Size|Large|Compact|Highly compressed|
|Schema|No|Required|Metadata included|
|Use Case|Simple, debug|Real-time pipelines|Analytics, big data|