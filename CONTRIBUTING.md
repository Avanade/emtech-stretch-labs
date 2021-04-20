# Contributing to the Labs
Thank you for your interest in contributing!

Please feel free to contribute code, ideas, improvements, and patches - we've added some general guidelines and information below, and you can propose changes to this document in a pull request.

## Rights to your contributions
By contributing to this project, you:
- Agree that you have authored 100% of the content
- Agree that you have the necessary rights to the content
- Agree that you have received the necessary permissions from your employer to make the contributions (if applicable)
- Agree that the content you contribute may be provided under the Project license(s)
- Agree that, if you did not author 100% of the content, the appropriate licenses and copyrights have been added along with any other necessary attribution.

## Code of Conduct
This project, and people participating in it, are governed by our [code of conduct](CODE_OF_CONDUCT.md). By taking part, we expect you to try your best to uphold this code of conduct. If you have concerns about unacceptable behaviour, please contact one of the project maintainers - right now, either [Chris](https://twitter.com/sealjay_clj) or [Fergus](https://twitter.com/FergusKidd).

## What should I know before I get started?
### Workflow
We're using the [standard GitHub workflow](https://guides.github.com/introduction/flow/), and asking our contributors to use [semantic commits](https://nitayneeman.com/posts/understanding-semantic-commit-messages-using-git-and-angular/#common-types) to support their contributions.

### Documentation
When we make changes to the project, including design changes, but also changes which require instructions, please consider you should add to the [documentation directory](https://github.com/Avanade/emtech-stretch-labs/tree/main/docs/).

# More information
## Semantic Commits and Commitizen
This repository uses [Commitizen](https://github.com/commitizen/cz-cli#making-your-repo-commitizen-friendly) to support the use of [semantic commits](https://nitayneeman.com/posts/understanding-semantic-commit-messages-using-git-and-angular/#common-types), which requires you to have node and commitizen installed, as well as the plugin we're using.  *Note, there are two similar projects called Commitizen. We're using the Node package, not the Python package.*

We use [cz-customizable](https://github.com/leoforfree/cz-customizable) to enforce a standard commit approach.
### Setting up Commitizen
You will need node installed on your local machine, or in your dev container.

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
## Workflow
### Project Members
Create a branch, based on the GitHub issue you're working on; making sure the issue number and title are correctly updated.

You can update your [VS Code settings](https://code.visualstudio.com/) and use the [GitHub Pull Requests plugin](https://aka.ms/vscodepr-download) to handle this automatically for you.
```
"githubIssues.issueBranchTitle": "${issueNumber}-${sanitizedIssueTitle}"
```

### External Contributors
- Create a fork.
- Create a branch `git checkout -b feature/featurename` with [a descriptive name].(https://guides.github.com/introduction/flow/), possibly including an issue you want to reference.
- Commit your changes `git commit -am 'Bug (scope): Fixed a bug'` with enough information to describe the commit.
- Push to the branch `git push`.
- Create a new [pull request](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/creating-an-issue-or-pull-request) for review when ready, relating to [an issue](https://guides.github.com/features/issues/).
- By raising a pull request, you agree you have the rights to contribute your changes.

### Pull Requests and Issues
We'll try to review all pull requests, and we'll try to follow this approach ourselves as a project.

Please check any issues raised on the pull request, like licensing issues for example.

We may add more information here over time.