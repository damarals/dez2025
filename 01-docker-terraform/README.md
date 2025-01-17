# Data Engineering Homework Solutions

## Module 1: Docker & SQL

### Question 1: Understanding Docker First Run

**Question**: When running Docker with the `python:3.12.8` image in interactive mode using bash as entrypoint, what is the pip version installed in the image?

**Options**:
- [x] 24.3.1
- [ ] 24.2.1
- [ ] 23.3.1
- [ ] 23.2.1

**Solution**:
```bash
docker run -it python:3.12.8 bash
pip --version # Output: pip 24.3.1
```

### Question 2: Understanding Docker Networking and Docker Compose

**Question**: In the given docker-compose.yaml file, what is the hostname and port that pgadmin should use to connect to the postgres database?

**Options**:
- [ ] postgres:5433
- [ ] localhost:5432
- [ ] db:5433
- [ ] postgres:5432
- [x] db:5432

**Explanation**:
- When services are in the same docker-compose file:
  - Use the service name (`db`) as hostname
  - Use the internal port (5432)
- Port mapping (5433:5432) is only relevant for external access

### Question 3: Trip Segmentation Count

**Question**: Count of trips by distance category between Oct 1st and Nov 1st 2019.

**Options**:
- [ ] 104,802; 197,670; 110,612; 27,831; 35,281
- [x] 104,802; 198,924; 109,603; 27,678; 35,189
- [ ] 104,793; 201,407; 110,612; 27,831; 35,281
- [ ] 104,793; 202,661; 109,603; 27,678; 35,189
- [ ] 104,838; 199,013; 109,645; 27,688; 35,202

**SQL Query**:
```sql
SELECT 
    COUNT(CASE WHEN trip_distance <= 1 THEN 1 END) as up_to_1_mile,
    COUNT(CASE WHEN trip_distance > 1 AND trip_distance <= 3 THEN 1 END) as "1_to_3_miles",
    COUNT(CASE WHEN trip_distance > 3 AND trip_distance <= 7 THEN 1 END) as "3_to_7_miles",
    COUNT(CASE WHEN trip_distance > 7 AND trip_distance <= 10 THEN 1 END) as "7_to_10_miles",
    COUNT(CASE WHEN trip_distance > 10 THEN 1 END) as over_10_miles
FROM 
    green_taxi_trips
WHERE 
    lpep_pickup_datetime >= '2019-10-01' 
    AND lpep_dropoff_datetime < '2019-11-01';
```

**Results**:
| up_to_1_mile | 1_to_3_miles | 3_to_7_miles | 7_to_10_miles | over_10_miles |
|--------------|--------------|--------------|----------------|---------------|
| 104802       | 198924       | 109603       | 27678          | 35189         |

### Question 4: Longest Trip for Each Day

**Question**: Which was the pick up day with the longest trip distance?

**Options**:
- [ ] 2019-10-11
- [ ] 2019-10-24
- [ ] 2019-10-26
- [x] 2019-10-31

**SQL Query**:
```sql
SELECT 
    DATE(lpep_pickup_datetime) as pickup_date,
    MAX(trip_distance) as max_distance
FROM
    green_taxi_trips 
GROUP BY
    DATE(lpep_pickup_datetime)
ORDER BY
    max_distance DESC
LIMIT 1;
```

**Results**:
| pickup_date | max_distance |
|-------------|--------------|
| 2019-10-31  | 515.89      |

### Question 5: Three Biggest Pickup Zones

**Question**: Which were the top pickup locations with over 13,000 in total_amount for 2019-10-18?

**Options**:
- [x] East Harlem North, East Harlem South, Morningside Heights
- [ ] East Harlem North, Morningside Heights
- [ ] Morningside Heights, Astoria Park, East Harlem South
- [ ] Bedford, East Harlem North, Astoria Park

**SQL Query**:
```sql
SELECT 
    tz."Zone" as pickup_zone,
    SUM(t."total_amount") as total_amount
FROM 
    green_taxi_trips t
JOIN 
    taxi_zones tz ON t."PULocationID" = tz."LocationID"
WHERE 
    t.lpep_pickup_datetime >= '2019-10-18' 
    AND t.lpep_pickup_datetime < '2019-10-19'
GROUP BY 
    tz."Zone"
HAVING 
    SUM(t."total_amount") > 13000
ORDER BY
    total_amount DESC;
```

**Results**:
| pickup_zone          | total_amount |
|---------------------|--------------|
| East Harlem North   | 18686.68     |
| East Harlem South   | 16797.26     |
| Morningside Heights | 13029.79     |

### Question 6: Largest Tip

**Question**: For passengers picked up in October 2019 in East Harlem North, which drop off zone had the largest tip?

**Options**:
- [ ] Yorkville West
- [x] JFK Airport
- [ ] East Harlem North
- [ ] East Harlem South

**SQL Query**:
```sql
SELECT 
    dropoff."Zone" as dropoff_zone,
    MAX(t."tip_amount") as max_tip
FROM 
    green_taxi_trips t
JOIN 
    taxi_zones pickup 
    ON t."PULocationID" = pickup."LocationID"
JOIN
    taxi_zones dropoff
    ON t."DOLocationID" = dropoff."LocationID"
WHERE 
    DATE(t.lpep_pickup_datetime) >= '2019-10-01'
    AND DATE(t.lpep_pickup_datetime) < '2019-11-01'
    AND pickup."Zone" = 'East Harlem North'
GROUP BY 
    dropoff."Zone"
ORDER BY 
    max_tip DESC
LIMIT 1;
```

**Results**:
| dropoff_zone | max_tip |
|--------------|---------|
| JFK Airport  | 87.3    |

### Question 7: Terraform Workflow

**Question**: What is the correct sequence for: downloading provider plugins and setting up backend, generating proposed changes and auto-executing the plan, and removing all resources managed by terraform?

**Options**:
- [ ] terraform import, terraform apply -y, terraform destroy
- [ ] teraform init, terraform plan -auto-apply, terraform rm
- [ ] terraform init, terraform run -auto-approve, terraform destroy
- [x] terraform init, terraform apply -auto-approve, terraform destroy
- [ ] terraform import, terraform apply -y, terraform rm

**Explanation**:
1. `terraform init`: Downloads provider plugins and sets up the backend
2. `terraform apply -auto-approve`: Generates and automatically applies the proposed changes
3. `terraform destroy`: Removes all resources managed by Terraform