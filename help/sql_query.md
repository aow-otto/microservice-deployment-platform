## Useful Queries

```sql
select * from SystemLog;
select * from SystemLog where timestamp >= date_sub(now(), interval 10 minute);
insert into SystemLog (level, message, component, subcomponent) values ('info', 'test', 'test component', 'test subcomponent');
```

```sql
select * from ServiceData;
select * from ServiceData where timestamp >= date_sub(now(), interval 10 minute);
insert into ServiceData (microservice, data) values ('test microservice', 'test');
select data from ServiceData where microservice = 'test microservice' order by timestamp desc limit 1;
```

```sql
select * from ServiceStatus;
select status from ServiceStatus where microservice = "test" order by timestamp desc limit 1;
```

```sql
select * from ServiceLog;
```

### Basics
```sql
use MicroserviceDeploymentPlatform;
delete from ServiceStatus;
describe ServiceStatus;
```