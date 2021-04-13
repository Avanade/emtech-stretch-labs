# Contributing
Please feel free to contribute code, ideas, improvements, and patches - please just make sure you follow a couple of guidelines.

## Commit Approach
This repository uses [Commitizen](https://github.com/commitizen/cz-cli#making-your-repo-commitizen-friendly) to support the use of [semantic commits](https://nitayneeman.com/posts/understanding-semantic-commit-messages-using-git-and-angular/#common-types), which requires you to have node and commitizen installed, as well as the plugin we're using.

We use [cz-customizable](https://github.com/leoforfree/cz-customizable) to enforce a standard commit approach.
### Setting up Commitizen
You will need node installed.

#### Install the required node packages globally
```bash
npm install -g commitizen
npm install -g cz-customizable
```
#### Create a global commitizen file
`echo '{ "path": "cz-customizable" }' > ~/.czrc`
This might clash if you use other cz plugins on other projects, like `cz-conventional-changelog`.
#### Usage
Run `git cz` when creating commits.

# Pull Requests
## Project Members
Create a branch, based on the GitHub issue you're working on; making sure the issue number and title are correclty updated.

You can update your VS Code settings and use the [GitHub Pull Requests plugin](https://aka.ms/vscodepr-download) to handle this automatically for you.
```
"githubIssues.issueBranchTitle": "${issueNumber}-${sanitizedIssueTitle}"
```

## External Contributors
- Create a fork.
- Create a feature branch `git checkout -b feature/featurename` in the [Gitflow style](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- Commit your changes `git commit -am 'Bug: Fixed a bug'` using
- Push to the branch `git push`.
- Create a new [pull request](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/creating-an-issue-or-pull-request) for review when ready, relating to [the issue](https://guides.github.com/features/issues/)
- If you haven't previously signed the CLA, you will be asked to sign.

# Contributor License Agreement
All contributions to this project must be accompanied by a signed [Contributor License Agreement](./docs/contributor-licence-agreement.md) ('CLA'); you (or the entity you're contributing on behalf of) retain your copyright, but the CLA gives us permission to use and redistribute your contributions as part of the project, and the open source licence that this project is using.

When you raise a pull request, you will be asked to sign a CLA on the pull request if you haven't previously signed the CLA.

# Reviews
All submissions will be reviewed, although some fixes may be contributed directly to /main if time is of the essence. Reviews are completed via GitHub.