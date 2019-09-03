# 🔰 Contributing to half_tael_DQN

> This file serves as the contributors' guidelines for the [half_tael_DQN](https://github.com/choH/half_tael_DQN) project.
>
> 📌 v3.0 | 2019.09.02 | Henry Zhong

---

As you are contributing to this project, it is assumed that you have your OANDA credentials assigned in [`oanda_config.py`](https://github.com/choH/half_tael_DQN/blob/master/oanda_config.py). To protect your privacy and to keep the integrity of this repository, please do:
```
git update-index --assume-unchanged oanda_config.py
```
So that `git` will stop tracking future changes to `oanda_config.py`.

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
| 🐛 | Bugfix | 📌 | Version tag  |
| 🔒 | Security Enhance | 🚚  | Move path  |
| 🐎  | Performance Enhance | 🗑️  | Removal  |
| 🚨 | Test | 💩  | Deprecation |
| 📊  | Data | ⏪  | Rewind |
| ⚙️  | Environment | 🔀  | Rebase / Merge |
| ⏲ | Tuning | 📦  | Pack |
| 📈  | Analysis | ✅ ☑️ ❌ ❓ | Review feedback |

**If one commit performs multiple tasks, use multiple Emojis with `<white space>` in between. Also leave a `<white space>` between the last Emoji and the text of commit message.**

### 1.2. Use imperative tone

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
From github.com:choH/half_tael_DQN
>>       * branch            YourBranch -> FETCH_HEAD
>>       Already up to date.
>>       Current branch YourBranch is up to date.
git rebase master
>>       Current branch YourBranch is up to date.
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

**With Section 2.4 or 2.5 done, `YourBranch` should have all the commits from `master` before its branch commits**

Go on GitHub web interface --> checkin `YourBranch` --> Click on `New pull request` besides `YourBranch` --> `Create pull request` -->  the expand arrow beside `Create a merge commit` (if applicable) --> `Rebase and merge`.

The method of `rebase` has many advantages, but one of its con is it will lose the information regarding which `commit` you branch was `checkout` from. Thus, you should title your pull request as:

```
Rebase <YourBranch> (from <commit hash you checkout from>) onto <BaseBranch>  <commit hash you rebase to>.
```



### 2.6. Declare branch out in the comment section of the commit you checked out from.

As mentioned, rebase will it will lose the information regarding which `commit` you branch was `checkout` from. Thus, it is recommend to go into comment section of the commit you check out from, and write something like:

```
Branch [YourBranch](link_to_your_branch) checked out from this commit.
```

### 2.7. Make an empty commit prefixed by 📌 to emphasis an important timestamp.

With the usage of `rebase`, the commit history of this project will be displayed in a linear manner, such as:

```
start-of-task-A --> A.1 --> A.2 --> A.x --> end-of-task-A --> start-of-task-B --> B.1 --> B.x --> end-of-task-B --> start-of-task-C
```

But real-life commit history won't have commits like `start-of-task-A` and `end-of-task-A`; in fact, it won't even have the `A.` or `B.` prefix to help you distinguish which task this commit is working for. Thus, it is recommend to mark out an important accomplishment (usually ganged with [issues](https://github.com/choH/half_tael_DQN/issues) or even [milestones](https://github.com/choH/half_tael_DQN/milestones)) with an empty commit prefix by `📌`.

To write an empty commit message prefixed by `📌`:
```
git commit --allow-empty -m "📌 Your commit message."
```

p.s. It is usually hard to pin the start of a task as development may lead to a various range of accomplishments. But if you are certain about it, you are more than welcome to pin it — e.g. we push a pin commit before every version release like [`📌 v2.0 pre release pin.`](https://github.com/choH/half_tael_DQN/commit/d0d5eac3563920ce8d73ecbd59ecc45611a0e532).

## 3. Examples

#### 3.1. Example for 2.5. | Pull request writing.

---

**[Rebase half_tael_v3.0 (from d0d5eac) onto master d0d5eac.](https://github.com/choH/half_tael_DQN/pull/16)**

Rebase branch [half_tael_v3.0](https://github.com/choH/half_tael_DQN/tree/half_tael_v3.0) onto master as milestone [half_tael_v3.0: Refactor DQN_v2.5 to work with virtual trading platform](https://github.com/choH/half_tael_DQN/milestone/5?closed=1) accomplished.

* From [d0d5eac](https://github.com/choH/half_tael_DQN/commit/d0d5eac3563920ce8d73ecbd59ecc45611a0e532)
* Onto [d0d5eac](https://github.com/choH/half_tael_DQN/commit/d0d5eac3563920ce8d73ecbd59ecc45611a0e532) (no update on master during the time).

---


#### 3.2. Example for 2.6. | Branch checkout comment writing.

---

**[📌 v2.0 pre release pin.](https://github.com/choH/half_tael_DQN/commit/d0d5eac3563920ce8d73ecbd59ecc45611a0e532)**

Branch [half_tael_v3.0](https://github.com/choH/half_tael_DQN/tree/half_tael_v3.0) checked out from this commit — a.k.a. [half_tale_DQN v2.0: Virtual Trading Platform with DQN v1.0 + DQN v2.5](https://github.com/choH/half_tael_DQN/releases/tag/v2.0).

---


