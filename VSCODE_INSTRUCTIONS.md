## Datafold VS Code Extension

This is a simple guide for installing the latest version of the VS Code 
extension. 
Please reach out to Leo and Jai by emailing leo@datafold.com and 
jai@datafold.com if you have any questions or feedback!

1. [Install the Extension using the VS Code Extension tab.](https://marketplace.visualstudio.com/items?itemName=Datafold.datafold-vscode)
<img width="320" alt="Screenshot 2023-07-05 at 14 36 46" src="https://github.com/datafold/demo/assets/1799931/ca13bce5-cee4-4c56-998c-a183fe3469df">

2. `cd` into your dbt project. 

3. `dbt build` or `dbt run` any models that you plan to edit or diff, to ensure
relevant development data models and dbt artifacts exist.

4. Use the command palate (⌘⇧P on Mac, ⌃⇧P on Windows and Linux) and install `data-diff` by
searching for "Datafold: Install data-diff package". 

- You'll be walked through a few steps including:
  - setting up your `dbt_project.yml`
  - setting the path to your `profiles.yml`
  - selecting a data warehouse
- **If you use custom schemas**, just enter any text string in the "Enter your schema" step. This will populate the `production_schema`
  `var` in your `dbt_project.yml` with whatever value you entered. Then, you'll need to adjust your `dbt_project.yml`
  following the steps in the Custom Schema section in [our documentation](https://docs.datafold.com/development_testing/open_source/).

5. Again use the command palate and search for "Datafold: Diff dbt model" to diff a specific model.

6. `dbt run` any models, using any selectors (like `+`). Then, try a new command: "Datafold: Diff latest dbt run results".

7. Click on the Datafold bird to view diff results from all the models that were diffed by "Diff latest dbt run results". You can click on the
little icons to view either value-level or summarized diff results.

<img width="600" alt="Screenshot 2023-07-05 at 14 39 59" src="https://github.com/datafold/demo/assets/1799931/aebc23c3-8e4e-438c-8529-d8fc9d810a7e">

8. Click on "More info" next to "Values" to see value-level differences.

<img width="600" alt="Screenshot 2023-07-05 at 14 40 13" src="https://github.com/datafold/demo/assets/1799931/f389c60d-9d54-4a75-a0c3-d81bbe2ccfc2">
