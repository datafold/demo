## Datafold VS Code
```
datafold-vscode v0.0.4
```

This is a simple guide for installing the latest version of the VS Code 
extension. 
Please reach out to Leo and Jai by emailing leo@datafold.com and 
jai@datafold.com if you have any questions or feedback!

1. Download the VSIX file the Datafold team provides you.
2. Open VS Code.
3. Click on Extensions.
   
<img width="400" alt="Screenshot 2023-06-29 at 15 26 29" src="https://github.com/datafold/demo/assets/1799931/0371275e-97ef-49a3-8dfb-74dea1555dba">

5. Click on the three dots and select "Install from VSIX".

<img width="400" alt="Screenshot 2023-06-29 at 15 27 49" src="https://github.com/datafold/demo/assets/1799931/d07c4cb8-5711-4d4e-9f72-cdb4efedff33">

6. Once installed, click on the extension to get oriented and read
7. about its current capabilities.

<img width="400" alt="Screenshot 2023-06-29 at 15 35 48" src="https://github.com/datafold/demo/assets/1799931/809c6580-3853-4673-b7aa-c86405057207">

7. `cd` into your dbt project. `dbt build` or `dbt run` any models that
8. you plan to edit or diff, to ensure relevant development
data models and dbt artifacts exist.
9. Use the command palate (⌘⇧P on Mac, ⌃⇧P on Windows and Linux) and
10. install data-diff if you haven't already by
searching for "Datafold: Install data-diff package". You'll be walked
through a few steps including setting up your `dbt_project.yml` and
setting the path to your `profiles.yml`.
12. Use the command palate and search for "Datafold: Diff dbt model"
13. to diff a specific model.
14. `dbt run` any arbitary models and then try "Datafold: Diff latest
15. dbt run results".
16. Click on the Datafold bird to select from models to diff using a GUI.
<img width="400" alt="Screenshot 2023-06-29 at 15 48 07" src="https://github.com/datafold/demo/assets/1799931/936be28b-7dce-4df3-aaf0-f8e2e9823cb0">
