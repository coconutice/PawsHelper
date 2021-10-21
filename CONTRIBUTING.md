# Contributing to PawsHelper

The PawsHelper welcomes contributions from the community. If you wish to contribute code please follow the below workflow to submit a pull request.


## GitHub Contribution Workflow

Developers work in their own forked copy of the repository and when ready,
submit pull requests to have their changes considered and merged into the
project's repository.

1. Fork your own copy of the repository to your GitHub account by clicking on
   `Fork` button on [PawsHelper GitHub repository](https://github.com/ChujieChen/PawsHelper).
2. Clone the forked repository on your local setup.
    ```
    git clone https://github.com/$user/PawsHelper.git
    ```
    Add a remote upstream to track upstream PawsHelper repository.
    ```
    git remote add upstream https://github.com/ChujieChen/PawsHelper.git
    ```
    Never push to upstream main
    ```
    git remote set-url --push upstream no_push
    ```
3. Create a topic branch.
    ```
    git checkout -b branchName
    ```
4. Make changes and commit it locally.
    ```
    git add <modifiedFile>
    git commit
    ```
5. Keeping branch in sync with upstream.
    ```
    git checkout branchName
    git fetch upstream
    git rebase upstream/main
    ```
6. Push local branch to your forked repository.
    ```
    git push -f origin branchName:remoteBranchName
    ```
7. Create a Pull request on GitHub.
   Visit your fork at `https://github.com/$user/PawsHelper` and click
   `Compare & Pull Request` button next to your `remoteBranchName` branch.

### Getting reviewers

Once you have opened a Pull Request (PR), reviewers will be assigned to your
PR and they may provide review comments which you need to address.
Commit changes made in response to review comments to the same branch on your
fork. Once a PR is ready to merge, `Squash and Merge` any *fix review feedback, typo*
and *merged* sorts of commits.
