# 🔰 Contributing to half_tael_DQN

> This file serves as the contributors' guidelines for the [half_tael_DQN](https://github.com/choH/half_tael_DQN) project.
>
> 📌 v1.0 | 2019.07.26 | Henry Zhong

---
## 1. Commit Message.

### 1.1 Prefix with emoji(s).


| **Emoji** | **Use Case** | **Emoji** | **Use Case** |
| :-: | :-: | :-: | :-: |
| 🎉 | Initial commit | 📚 | Documentation |
| ✨ | New feature | 💄 | Cosmetic |
| 🔨 | Update | 📡 | Broadcast |
| ♻️ | Refactor | 🔰 | User manual |
| 🚧 | Work in progress | 💡  | Idea |
| 🐛 | Bugfix | 📌  | Version tag  |
| 🔒 | Security Enhance | 🚚  | Move path  |
| 🐎  | Performance Enhance | 🗑️  | Removal  |
| 🚨 | Test | 💩  | Deprecation |
| 📊  | Data | ⏪  | Rewind |
| ⚙️  | Environment | 🔀  | Rebase / Merge |
| ⏲ | Tuning | 📦  | Pack |
| 📈  | Analysis | ✅ ☑️ ❌ ❓ | Review feedback |

**If one commit performs multiple tasks, use multiple Emojis with `<white space>` in between. Also leave a `<white space>` between the last Emoji and the text of commit message.**

### 1.2. Imperative Tone

> Describe your changes in imperative mood, e.g. "make xyzzy do frotz" instead of "[This patch] makes xyzzy do frotz" or "[I] changed xyzzy to do frotz", as if you are giving orders to the codebase to change its behavior.
> -- [SubmittingPatches\Documentation](https://git.kernel.org/pub/scm/git/git.git/tree/Documentation/SubmittingPatches?id=HEAD#n133)

---
## 2. Version Control with Git `branch` and `rebase`.


### 2.1.Creating your new branch.
```
git checkout master
git checkout -b YourBranch                  # new branch base on master.
git checkout -b YourBranch v1.0             # new branch base on release tag.
git checkout -b YourBranch ExistedBranch    # new branch base on existed branch.

git push origin YourBranch                  # push YourBranch to repository.
```

### 2.2. Developing on your branch.
```
git checkout YourBranch
git add ModifiedFile
git commit -m "Emoji Commit Message"
git push -u origin YourBranch
```

### 2.3. Update your branch with master by using `rebase` (without conflict).
```
git checkout YourBranch
git pull origin YourBranch --rebase
git rebase master
git push origin YourBranch -f
```


### 2.4 Update your branch with master by using `rebase` (with conflict).
```
git checkout YourBranch
git pull origin YourBranch --rebase
git rebase master
git status
>>       both modified:   a_file
atom a_file                           # or open with any other editor, as long as you resolve the conflict(s).
git add a_file
git rebase --continue
>>      If there is nothing left to stage, chances are that something else
>>      already introduced the same changes; you might want to skip this patch.
git rebase --skip                    # If the terminal show no above message, you may skip this comnand.
git push origin YourBranch -f
```
The usage of `git rebase --skip` is a bit unintuitive, you may refer [this article](http://wholemeal.co.nz/blog/2010/06/11/no-changes-did-you-forget-to-use-git-add/) as an extended reading.




### 2.5. Make pull request to rebase and merge your branch into master.

**With Section 2.4 or 2.5 done, `YourBranch` should have all the commits from `master`**

Go on GitHub web interface, Click on `Compare & pull request` besides `YourBranch` --> `Create pull request` -->  the expand arrow beside `Create a merge commit` --> `Rebase and merge`.

The method of `rebase` has many advantages, but one of its con is it will lose the information of which `commit` you branch was `checkout` from. Thus, in the pull request message, you should always write something like:

```
🔀 RM <YourBranch> (from <commit hash you checkout from>) to <BaseBranch>  <commit hash you rebase to>.
```
`<BaseBranch>` is usually master.





