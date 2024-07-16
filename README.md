# Datafold Demo Project

This repo contains a demo project suited to leveraging Datafold:
- dbt project that includes
  - raw data (implemented via [seed CSV files](https://docs.getdbt.com/docs/building-a-dbt-project/seeds)) from a fictional app
  - a few downstream models, as shown in the project DAG below
- several 'master' branches, corresponding to the various supported cloud data platforms
  - `master` - 'primary' master branch, runs in Snowflake
  - `master-databricks` - 'secondary' master branch, runs in Databricks, is reset to the `master` branch daily or manually when needed via the `branch_replication.yml` workflow
- several GitHub Actions workflows illustrating CI/CD best practices for dbt Core
  - dbt PR job - is triggered on PRs targeting the `master` branch, is executed in Snowflake
  - dbt prod - is triggered on pushes into the `master` branch, is executed in Snowflake
  - dbt PR job (Databricks) - is triggered on PRs targeting the `master-databricks` branch, is executed in Databricks
  - dbt prod (Databricks) - is triggered on pushes into the `master-databricks` branch, is executed in Databricks
- raw data generation tool to simulate a data flow typical for real existing projects

<p align="center">
    <img src="img/demo_project_dag.png" width="750">
</p>

## Running this project in the pre-configured Datafold environment

### Code management
All actual changes should be commited to the `master` branch, other `master-...` branches are supposed to be reset to the `master` branch daily.

### Demonstration
To demonstrate Datafold experience in CI on Snowflake - one needs to create PRs targeting the `master` branch.
- production schema in Snowflake: `demo.core`
- PR schemas: `demo.pr_num_<pr_number>`

To demonstrate Datafold experience in CI on Databricks - one needs to create PRs targeting the `master-databricks` branch.
- production schema in Databricks: `demo.default`
- PR schemas: `demo.pr_num_<pr_number>`

Corresponding Datafold Demo Org contains the following integrations:
- `Snowflake` data connection
- `Coalesce-Demo` CI integration for the `Snowflake` data connection and the `master` branch
- `Databricks-Demo` data connection
- `Coalesce-Demo-Databricks` CI integration for the `Databricks-Demo` data connection and the `master-databricks` branch
- `Postgres` data connection for Cross-DB data diff monitors

### Data replication simulation

To demonstrate Datafold functionality for data replication monitoring, a pre-configured Postgres instance is populated with 'correct raw data' (`analytics.data_source.subscription_created` table); the `subscription__created` seed CSV file contains 'corrupted raw data'.

## Running this project in custom environment
To get up and running with this project:
1. Install dbt using [these instructions](https://docs.getdbt.com/docs/installation).

2. Fork this repository.

3. Set up a profile called `demo` to connect to a data warehouse by following [these instructions](https://docs.getdbt.com/docs/configure-your-profile). You'll need `dev` and `prod` targets in your profile.

4. Ensure your profile is setup correctly from the command line:
```bash
$ dbt debug
```

5. Create your `prod` models:
```bash
$ dbt build --profile demo --target prod
```

With `prod` models created, you're clear to develop and diff changes between your `dev` and `prod` targets.

### Using Datafold with this project

Follow the [quickstart guide](https://docs.datafold.com/quickstart_guide) to integrate this project with Datafold.

## Generated data

### Generated files
- `datagen/feature_used_broken.csv` - copied to `seeds/feature__used.csv`
- `datagen/feature_used.csv`
- `datagen/org_created_broken.csv` - copied to `seeds/org__created.csv.csv`
- `datagen/org_created.csv`
- `datagen/signed_in_broken.csv` - copied to `seeds/signed__in.csv.csv`
- `datagen/signed_in.csv`
- `datagen/subscription_created_broken.csv` - copied to `seeds/subscription__created.csv.csv`
- `datagen/subscription_created.csv` - pushed to Postgres
- `datagen/user_created_broken.csv` - copied to `seeds/user__created.csv.csv`
- `datagen/user_created.csv`
- `datagen/persons_pool.csv` - pool of persons used for user/org generation

### Data generation scripts

- `datagen/data_generate.py` - main data generation script
- `datagen/data_to_postgres.sh` - pushes generated data to Postgres 
- `datagen/persons_pool_replenish.py` - replenishes the pool of persons using ChatGPT
- `datagen/data_delete.sh` - deletes data for further re-generation


### Data anomaly types
- zero on negative prices in the `subscription__created` seed
- corrupted emails in the `user__created` seed (user$somecompany.com)
- irregular spikes in the workday seasonal daily number of sign-ins in the `signed__in` seed
- `null` spikes in the `feature__used` seed
