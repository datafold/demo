# data-diff-demo
Demo of data-diff with a dbt project using dbt-duckdb

## Prerequisites

Verify that both `python3` and `git` are installed and available:
```shell
python3 --version
git --version
```

## Clone

Clone this repo using HTTPS (or [your method of choice](docs/clone.md)):

```shell
git clone https://github.com/datafold/demo.git
cd demo
```

</details>

## Install
Create a virtual environment and install dependencies using `bash`/`zsh` (or [your OS shell of choice](docs/virtual-environment.md)):

```shell
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
source env/bin/activate
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

```
dbt run -s dim_orgs+ --profiles-dir ./ && data-diff --dbt --dbt-profiles-dir .
```

Example output:
```diff
Found 4 successful model runs from the last dbt command.
146 rows in table A
157 rows in table B
0 rows exclusive to table A (not present in B)
11 rows exclusive to table B (not present in A)
112 rows updated
34 rows unchanged
78.34% difference score

Extra-Info:
  diff_counts = {'org_id_a': 5, 'num_users_a': 5, 'sub_plan_a': 2, 'sub_created_at_a': 2, 'sub_price_a': 2, 'created_at_a': 5}
  exclusive_count = 5
  table1_count = 146
  table1_sum_num_users = 452
  table1_sum_sub_price = 13752
  table2_count = 157
  table2_sum_num_users = 475
  table2_sum_sub_price = 14847
  validated_unique_keys = [['org_id'], ['org_id']]
```

## Wrap up
Deactivate the virtual environment when finished:

```shell
deactivate
```