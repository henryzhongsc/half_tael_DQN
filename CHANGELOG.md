# CHANGELOG

> This file serves as the journal for the [half_tael_DQN](https://github.com/choH/half_tael_DQN) project.

---
## Broadcast

### Upcoming Meetings:
* **2019-07-19 | Scrum | Henry, Jian, Steven** — Checkout **Meeting** section for details.


### 2019-07-10 | A short style guide for updating this `CHANGELOG.md`.
* The `CHANGELOG.md` has three sections.
    * **Broadcast**: Briefing of upcoming events or reminders (like this one).
    * **Meeting**: Summaries for meetings.
    * **Development Journal**: Records for development updates.
* For the sake of consistency, I suggest we update this `CHANGELOG.md` in a date descending order (new-to-old) with a headline format of `YYYY-MM-DD | Highlight | Name`. Note the `Highlight` and `Name` parts can be omitted if not applicable, e.g.
    * This broadcast headline, which omits `Name`.
    * Under **Development Journal** as `2019-04-10 | Henry Zhong`, which omits `Highlight`.

---
## Meeting

### 2019-07-19 | Scrum | Henry, Jian, Steven
* **Goal:**
    * ALL: Get familiar with Q-learning and DQN concept in general.
    * Henry: Build a basic wrapper base on [OANDA](https://www.oanda.com/us-en/) API for future input of the model.
    * Steven: Run a trial DQN model on SP500 data
    * Jian: Research and present some insight regarding the possible designs of DQN model.


### 2019-07-10 | Kick-off briefing | Anul Sinha, Henry, Jian, Steven
* Anul gave a presentation of his `forex` side-project, mainly regarding the method of interaction with OANDA, his model try-out, and why he abandoned this project.
* Due to the lacks of documentation of Anul's work, we decided to not to take over his project (also because he has moved on to a more combined design base on his `forex`), but to build our own bot. However, we will take his code as an important reference, especially regarding the OANDA API part and model environment setup.

---
## Development Journal

### 2019-07-11 | Finished Q-learning Courses | Henry
* Finished the *Q-learning* section of the [Morvan](https://morvanzhou.github.io/tutorials/machine-learning/reinforcement-learning/) course.
* Started the DQN section.
* Hand over the pervious project to be fully committed on this one.