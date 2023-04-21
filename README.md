# Datafold Demo Project

A demo project showcasing Datafold's open source data-diff and Single Player Cloud.

## Prerequisites

1. Ask the PX team for access to our demo organization (Datafold Org: Coalesce Demo).
2. Verify that `dbt`, `python3`, and `git` are installed and available:
    ```shell
    dbt --version
    python3 --version
    git --version
    ```

***Note***: If you don't have `dbt` installed, follow [these instructions](https://docs.getdbt.com/docs/installation).

## Getting Started

1. Clone this repo
2. Open the project
    ```bash
    cd demo
    ```
3. Make a new branch off on this branch
    ```bash
    git pull
    git checkout -b <my_demo_branch> will-dev
    ```
4. Set up environment variables
    - Add Demo Account *Environment Variables* (in PX Team's Password Vault)
        ```bash
        export SNOWFLAKE_ACCOUNT=...
        export SNOWFLAKE_USER=...
        export SNOWFLAKE_PASSWORD=...
        export SNOWFLAKE_ROLE=...
        export SNOWFLAKE_SCHEMA="DEV_<your_name>"
        ```
    - Generate API Key and add as environment variable
        - **Settings** -> **Account** then click "Generate API Key". Copy and paste the key with the command below.
        -   ```bash
            export DATAFOLD_API_KEY=XXXXXXXXX 
            ```

## Setup

Establish the baseline production tables:
```shell
dbt build --full-refresh --target prod --profiles-dir ./
```

Establish the baseline dev tables:
```shell
dbt build --full-refresh --profiles-dir ./
```

## Usage

Simulate a change to the table during development:

Go to `models/core/dim_orgs.sql` and comment out the `prod` CTE for the `dev` CTE

Run a single model & diff
```
dbt run -s dim_orgs --profiles-dir ./ && data-diff --dbt --dbt-profiles-dir .
```

Run model + all downstreams & diff
```
dbt run -s dim_orgs+ --profiles-dir ./ && data-diff --dbt --dbt-profiles-dir .
```

Run a single model & diff with Cloud
```
dbt run -s dim_orgs --profiles-dir ./ && data-diff --dbt --cloud --dbt-profiles-dir .
```
