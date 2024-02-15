<p align="center">
</p>
<p align="center">
    <h1 align="center">pyCoopGame</h1>
</p>
<p align="center">
    <em>Profit Allocation Methods</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/flechtenberg/pyCoopGame?style=flat&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/flechtenberg/pyCoopGame?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/flechtenberg/pyCoopGame?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/flechtenberg/pyCoopGame?style=flat&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/Jupyter-F37626.svg?style=flat&logo=Jupyter&logoColor=white" alt="Jupyter">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
</p>
<hr>

##  Quick Links

> - [ Overview](#-overview)
> - [ Features](#-features)
> - [ Repository Structure](#-repository-structure)
> - [ Modules](#-modules)
> - [ Getting Started](#-getting-started)
>   - [ Installation](#-installation)
> - [ Contributing](#-contributing)
> - [ License](#-license)
> - [ Acknowledgments](#-acknowledgments)

---

##  Overview

pyCoopGame is a powerful cooperative game theory library that provides various functionalities for building, solving, and analyzing cooperative games. It allows users to create random n-player TU games, validate the game structures, and calculate important measures such as the Shapley value, Nucleolus, Cost Gap, and epsilon-Core. The library includes modules for defining the game model, constraints, objective functions, and methods for checking the existence and calculating the least core and minmax core of a game. With its comprehensive set of features, pyCoopGame simplifies the process of studying and understanding cooperative games, making it an essential tool for researchers and practitioners in the field of cooperative game theory.

---

##  Features

|    |   Feature         | Description |
|----|-------------------|---------------------------------------------------------------|
| ⚙️  | **Architecture**  | The project follows a modular architecture, with separate modules for building and solving utility exchange networks, calculating the Shapley value, Nucleolus, Cost Gap, and epsilon-Core. The architecture promotes code reusability and easy maintenance. |
| 🔩 | **Code Quality**  | The code follows PEP8 style guidelines and maintains good readability. It demonstrates good code organization and uses meaningful function and variable names. |
| 📄 | **Documentation** | The project includes moderate documentation, with explanations of each module and their functionality. However, it could benefit from more detailed usage examples and comprehensive API documentation. |
| 🔌 | **Integrations**  | The project does not have any notable external integrations or dependencies besides standard Python libraries such as NumPy and Pandas for data manipulation. |
| 🧩 | **Modularity**    | The codebase exhibits good modularity. Each functionality is encapsulated in separate modules, allowing for easy expansion and reuse in other projects. |
| 🧪 | **Testing**       | The project lacks unit tests or testing frameworks, which could be improved to enhance code reliability and maintainability. |
| ⚡️  | **Performance**   | The performance of the project should be acceptable for most use cases. However, without specific benchmarks or optimizations, it may not scale well for large-coalition games. |
| 🛡️ | **Security**      | The project does not involve sensitive data or user access, so security measures are not a concern in this context. |
| 📦 | **Dependencies**  | The project has no external dependencies beyond standard Python libraries. |


---

##  Repository Structure

```sh
└── pyCoopGame/
    ├── LICENSE
    ├── notebooks
    │   └── Testing.ipynb
    ├── pyCoopGame
    │   ├── __init__.py
    │   ├── Core.py
    │   ├── CostGap.py
    │   ├── Create_game.py
    │   ├── Nucleolus.py
    │   ├── Shapley.py
    │   └── Validate_game.py
    ├── README.md
    └── setup.cfg
```

---

##  Modules

<details closed><summary>notebooks</summary>

| File                                                                                            | Summary                                                                                                                                                                                                                                                                                                                       |
| ---                                                                                             | ---                                                                                                                                                                                                                                                                                                                           |
| [Testing.ipynb](https://github.com/flechtenberg/pyCoopGame/blob/master/notebooks\Testing.ipynb) | This code snippet in the Testing.ipynb notebook is used to test and validate the functionality of the pyCoopGame library. It creates a random 3-player game, validates the game, checks if the core is empty, and calculates the Shapley value, Nucleolus, Cost Gap, and epsilon-Core. The results are stored in a dataframe. |

</details>

<details closed><summary>pyCoopGame</summary>

| File                                                                                                   | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ---                                                                                                    | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| [Core.py](https://github.com/flechtenberg/pyCoopGame/blob/master/pyCoopGame\Core.py)                   | The `Core.py` file in the `pyCoopGame` repository contains functions related to building and solving an abstract model of a utility exchange network. It defines the model structure, constraints, objective functions, and provides methods for checking the existence and calculating the least core and minmax core of a game.                                                                                                                                                                         |
| [CostGap.py](https://github.com/flechtenberg/pyCoopGame/blob/master/pyCoopGame\CostGap.py)             | The code snippet in `CostGap.py` is a function `tauvalue(game)` that calculates the tau value in cooperative game theory. It takes a game as input and performs calculations to determine the tau value for each player. The code extracts the set of players, changes the data type of coalitions, finds the grand coalition, determines marginal profits, calculates the minimum claim, determines alpha, and finally computes the tau value for each player. The function then returns the tau values. |
| [Create_game.py](https://github.com/flechtenberg/pyCoopGame/blob/master/pyCoopGame\Create_game.py)     | This code snippet `Create_game.py` is part of the `pyCoopGame` repository. It contains a function that creates a random n-player TU game and returns it as a DataFrame. The function generates all possible coalitions and assigns random benefits to each coalition. It also sets a random seed if provided.                                                                                                                                                                                             |
| [Nucleolus.py](https://github.com/flechtenberg/pyCoopGame/blob/master/pyCoopGame\Nucleolus.py)         | The code snippet in pyCoopGame/Nucleolus.py defines functions for creating and solving an optimization model to calculate the nucleolus of a cooperative game. The functions build and instantiate the model, solve it using a specified solver, and return the nucleolus values. There are also functions for comparing nucleolus values and ranking them based on a set of deltas.                                                                                                                      |
| [Shapley.py](https://github.com/flechtenberg/pyCoopGame/blob/master/pyCoopGame\Shapley.py)             | The Shapley.py code in the pyCoopGame repository calculates the Shapley value for each player in a cooperative game. It uses a difference in gains approach to determine the contribution of each player to every possible coalition. The result is returned as a dictionary.                                                                                                                                                                                                                             |
| [Validate_game.py](https://github.com/flechtenberg/pyCoopGame/blob/master/pyCoopGame\Validate_game.py) | The code in Validate_game.py validates the style of a passed dataframe for a cooperative game. It checks the format, data types, number of players, and other properties to ensure the dataframe is correctly structured. The code outputs messages indicating the correctness of the dataframe based on the validation checks performed.                                                                                                                                                                 |

</details>

---

###  Installation

It is recommended to install the package via
```
pip install git+https://github.com/flechtenberg/pyCoopGame
```

It is also possible to install a version using 
```
pip install pycoopgame
```
But there are some known issues with that version. Soon a new package release will replace this obsolete version.

###  Running `pyCoopGame`



##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/flechtenberg/pyCoopGame/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/flechtenberg/pyCoopGame/discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github.com/flechtenberg/pyCoopGame/issues)**: Submit bugs found or log feature requests for the `pyCoopGame` project.

<details closed>
    <summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/flechtenberg/pyCoopGame
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

##  License

This project is licensed under the `ℹ️  BSD 3-Clause` License. See the [LICENSE](LICENSE) file for additional info.
Copyright (c) 2024, Fabian Lechtenberg. All rights reserved.

---

##  Acknowledgments

...

[**Return**](#-quick-links)

---
