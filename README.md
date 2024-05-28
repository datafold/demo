# Datafold Demo Project

This repo contains a demo dbt project suited to leveraging Datafold.


### What's in this repo?
This repo contains [seeds](https://docs.getdbt.com/docs/building-a-dbt-project/seeds) that includes fake raw data from a fictional app.

This project includes raw data from the fictional app, and a few downstream models, as shown in the project DAG:

<p align="center">
    <img src="img/demo_project_dag.png" width="750">
</p>


### Running this project
To get up and running with this project:
1. Install dbt using [these instructions](https://docs.getdbt.com/docs/installation).

2. Fork this repository.

3. Change into the `demo` directory from the command line:
```bash
$ cd demo
```

4. Set up a profile called `demo` to connect to a data warehouse by following [these instructions](https://docs.getdbt.com/docs/configure-your-profile). You'll need `dev` and `prod` targets in your profile.

5. Ensure your profile is setup correctly from the command line:
```bash
$ dbt debug
```

6. Create your `prod` models:
```bash
$ dbt run --target prod
```

With `prod` models created, you're clear to develop and diff changes between your `dev` and `prod` targets.

### Using Datafold with this project

Follow the [quickstart guide](https://docs.datafold.com/quickstart_guide) to integrate this project with Datafold.

trigger
