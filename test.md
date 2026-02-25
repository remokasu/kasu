--- stacker/LICENSE ---
MIT License

Copyright (c) 2023 @remokasu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


--- stacker/CHANGELOG.md ---
# CHANGE LOG

## [1.9.1] - 2024-12-25

### Fixed

- **Void Function Support**:
  - Fixed critical bug where functions with no return value would crash with `IndexError`
  - Introduced `VOID` sentinel value to distinguish void functions from functions returning `None`
  - Void functions no longer pollute the stack with unnecessary values
  - Recursive void function calls no longer require `drop` operator
  - Example: `{msg} {msg echo} print defun` now works without crashing

### Changed

- **Function Return Value Behavior**:
  - Functions that produce no stack values now return `VOID` instead of crashing
  - `VOID` is not pushed to the stack, keeping stack clean
  - Explicit `None` values can still be used and will be pushed to stack normally

## [1.9.0] - 2024-12-25

### Added

- **Parentheses `()` for Code Blocks**:
  - `()` can now be used in place of `{}` for code blocks
  - Example: `(1 2 +) eval`, `(x y) (x y *) mul defun`

- **Variable Prefix `$` is Optional**:
  - Variables can be used without `$` prefix (old syntax `$x` still works)
  - `=` operator added as an alias for `set`
  - Example: `5 x =` and `x echo`

- **Global Variables**:
  - New `global` keyword for global variable declaration
  - Syntax: `value variable global`
  - Example: `0 counter global`

- **VSCode Syntax Highlighting**:
  - Syntax highlighting extension for `.stk` files
  - Auto-closing pairs, code folding, comment toggling
  - Installation: `cp -r .vscode-extension ~/.vscode/extensions/stacker-language`

### Changed

- **Performance Optimization**:
  - Improved function call performance with scope chain implementation

- **Examples Directory**:
  - Reorganized into categories: `basics/`, `functions/`, `algorithms/`, `advanced/`
  - Updated to use new syntax (no `$` prefix)

### Fixed

- Fixed comment parsing when `#` appears mid-line
- Enhanced error messages
- Fixed multiline `()` code blocks in script files


## [1.8.3]

### Bug Fixes

- **Fixed File Naming Typos**:
  - Renamed `stacker/exec_modes/excution_mode.py` to `execution_mode.py`
  - Fixed method name typo: `disp_all_valiables()` → `disp_all_variables()`
  - Fixed attribute name typo: `self.oprerators` → `self.operators` (affected 16+ locations in core.py)

- **Code Cleanup**:
  - Removed unused file `stacker/valiable.py` (all content was commented out)

### Changed

- **Improved Package Configuration**:
  - Updated `pyproject.toml` to properly specify all subpackages
  - Added explicit Python version requirement: `requires-python = ">=3.10"`
  - Updated dependency specification: `prompt-toolkit>=3.0.0`
  - Corrected `package-data` to only include actual data files


## [1.8.2]

- **Changed**

  Stopped using the deprecated pkg_resources module in favor of standard library alternatives.


## [1.8.1]

### Improvements
- **Increased Maximum Regression Iterations**: The maximum number of regression iterations has been increased.
- **Improved Token Interpretation**: Tokens enclosed in `{}` are now correctly interpreted even when there are no spaces between them.
  Example: `{x} {x 2 ^} lambda` is now interpreted as `{x}{x 2 ^}lambda`.

### New Features
- **`frac` Command**:
  Example: `3 4 frac` returns `Fraction(3, 4)` and displays as `3/4`.
- **File Commands**:
  - `write-to-file`: Writes specified content to a file.
    Example: `"This is a test file." "test.txt" write-to-file`
  - `append-to-file`: Appends specified content to a file.
    Example: `"This is a test file." "test.txt" append-to-file`
  - `read-from-file`: Reads content from a file.
    Example: `"test.txt" read-from-file`
  - `file-exists`: Checks if a file exists.
    Example: `"test.txt" file-exists`

### Documentation Fixes
- Fixed incorrect explanation for the `read` command in `README.md`.


## [1.8.0]

- **Breaking Changes**

  - **Modified ifelse Syntax**:

    Before: <true-expr> <false-expr> condition ifelse
    After: condition <true-expr> <false-expr> ifelse

    Note: This change is not backwards compatible with previous versions.

  - **Modified if Syntax**:

    Before: <true-expr> condition if
    After: condition <true-expr> if

    Note: This change is not backwards compatible with previous versions.

- **Bug Fixes**

  Fixed variable scope handling in recursive function processing


## [1.7.0]

- **Support for Lambda Functions**:
  - Lambda functions are now supported, enabling inline definitions and executions of anonymous functions.
  - **Example**:
    ```
    stacker:0> {x} {x 2 *} lambda
    ```

- **Enforced Symbol Naming Conventions**:
  - Symbols used as arguments in `set`, `defun`, and `defmacro` now require a `$` prefix to improve clarity and prevent naming conflicts.
  - **Example**:
    ```
    stacker:0> 123 $a set
    ```

- **New Stack Manipulation Commands**:
  - **n listn**: Converts the top n elements from the stack into a list.
  - **extend**: Expands list objects onto the stack.

- **Input/Output Enhancements**:
  - **read**: Reads data from standard input.
  - **read-from-string**: Interprets a string as RPN expressions and reads it.

- **Bug Fixes**:
  - Resolved an issue where unnecessary values were being pushed onto the stack during function execution in sub-blocks, causing unexpected errors during recursive operations.

- **Display Command Improvement**:
  - The `disp` command has been updated to omit commas between elements, aligning with REPL mode display conventions.

- **New Command**:
  - **abort**: Immediately terminates the program with an exit status of 1, equivalent to `exit(1)`.

- **Unified Line Endings**:
  - Line endings across files have been unified; `.gitattributes` has been updated with `* text=auto`.

- **Comment Handling Improvement**:
  - Fixed an oversight where text following a `#` in the middle of a line was not being recognized as a comment.


## [1.6.1]

### Bug Fixes
- Resolved an issue where passing arrays to user-defined functions resulted in errors.

### Breaking Changes
- Changed the macro definition command from `alias` to `defmacro`.
  - Rationale: This change aligns the macro definition syntax with the function definition syntax (`defun`).
  - Note: This modification is not backwards compatible with previous versions.

### Migration
Users will need to update their existing macro definitions:
- Old syntax: `alias`
- New syntax: `defmacro`


--- stacker/pyproject.toml ---
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "pystacker"
version = "1.9.2"
authors = [
    {name = "remokasu"}
]
description = "Stacker: RPN Calculator in Python"
readme = "README.md"
license = {file = "LICENSE"}
keywords = ["reverse-polish-calculator", "rpn", "terminal-app"]
requires-python = ">=3.10"
dependencies = ["prompt-toolkit>=3.0.0"]

[project.urls]
Homepage = "https://github.com/remokasu/stacker"

[project.scripts]
stacker = "stacker.__main__:main"

[tool.setuptools]
packages = [
    "stacker",
    "stacker.engine",
    "stacker.runtime",
    "stacker.runtime.exec_modes",
    "stacker.include",
    "stacker.lib",
    "stacker.operators",
    "stacker.manager",
    "stacker.plugins",
    "stacker.slib",
    "stacker.syntax",
    "stacker.util",
]
package-data = {"stacker" = [
    "data/*",
]}

--- stacker/README.md ---
# Stacker: An RPN Calculator and Extensible Programming Language

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Stacker is a powerful Reverse Polish Notation (RPN) calculator built with Python, featuring basic mathematical operations and extensibility through plugins.

## Table of Contents

- [Installation](#installation)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Running Scripts](#running-scripts)
- [VSCode Syntax Highlighting](#vscode-syntax-highlighting)
- [Error Formatting](#error-formatting)
- [Command Line Execution](#command-line-execution)
- [Configuration File](#configuration-file)
- [Creating Plugins](#creating-plugins)
- [Supported Operations](#supported-operations)

## Installation

```bash
git clone git@github.com:remokasu/stacker.git
cd stacker
pip install .
```

### Optional: VSCode Syntax Highlighting

For syntax highlighting support in VSCode:

```bash
cp -r .vscode-extension ~/.vscode/extensions/stacker-language
```

Reload VSCode (Ctrl+Shift+P → "Developer: Reload Window") and `.stk` files will be highlighted. 


## Dependencies

Python Prompt Toolkit is required for Stacker. Install it using the following command:
```bash
pip install prompt_toolkit
```

## Feedback and Contributions

Feedback and contributions are welcome. Please submit issues or suggestions on the [Issues page](https://github.com/remokasu/stacker/issues).


## Usage

Run Stacker:
```bash
stacker
```
Or:
```bash
python -m stacker
```

Stacker supports standard arithmetic operations (+, -, *, /) and advanced functions (sin, cos, tan, etc.). Users can input commands in RPN format and extend functionality using custom plugins.

### Input Examples

Stacker allows for straightforward RPN input. For example:

- Single-line input:
  ```bash
  stacker:0> 3 4 +
  [7]
  ```

- Multi-line input:
  ```bash
  stacker:0> 3
  [3]
  stacker:1> 4
  [3, 4]
  stacker:2> +
  [7]
  ```

- ### Numbers:
  The Stacker command allows you to directly push integers, floating-point numbers, and complex numbers onto the stack. This facilitates easy management of various types of numerical data.

  - Integers:
    ```bash
    stacker:0> 3
    [3]
    ```
    In this example, the integer 3 is added to the stack.

  - Floating-Point Numbers:
    ```bash
    stacker:1> 3.14
    [3.14]
    ```
    Here, the floating-point number 3.14 is added to the stack.

  - Complex Numbers:
    ```bash
    stacker:2> 1+2j
    [(1+2j)]
    ```
    In this case, the complex number 1+2j (with a real part of 1 and an imaginary part of 2) is added to the stack. Complex numbers are denoted by combining the real and imaginary parts with a +, and the imaginary part is indicated using j.

- ### Strings:
  - syntax:
    ```bash
    "Hello, World!"
    ```
  - example:
    ```bash
    stacker:0> "Hello, World!"
    ["Hello, World!"]
    ```
    In this example, the string "Hello, World!" is added to the stack.


- ### Variables:
  - syntax:
    ``` bash
    value name set
    # or
    value name =
    ```
  - example:
    ```bash
    stacker:0> 3 x set
    stacker:1> x
    [3]

    # Using = operator (equivalent to set)
    stacker:2> 5 y =
    stacker:3> y
    [5]
    ```
    In this example, we assign `3` to `x` using `set`, and `5` to `y` using `=`. Both operators work identically.

    **Note:** The `$` prefix (e.g., `$x`) is supported for backward compatibility but no longer required.

    **Note:** The `=` operator is an alias for `set` and can be used interchangeably. Use whichever feels more natural for your coding style.

    **Important:** Avoid using built-in operator names (like `sum`, `max`, `min`) as variable names,
    as this will shadow the operator. See [VARIABLE_NAMING.md](VARIABLE_NAMING.md) for details.

- Arrays:
  - Single-line array:
    ```bash
    stacker:0> [1 2 3; 4 5 6]
    [[1, 2, 3], [4, 5, 6]]
    ```

  - Multi-line array:
    ```bash
    stacker:0> [1 2 3;
    ... > 4 5 6]
    [[1, 2, 3], [4, 5, 6]]
    ```


- ### Code Blocks

  Code blocks are fundamental structures in Stacker that enable deferred evaluation and control flow management. They are enclosed in curly braces `{}`.

  **Syntax:**
  ```bash
  {code_elements}
  ```

  **Key Characteristics:**
  1. **Deferred Evaluation**: Code blocks are not executed immediately when encountered
  2. **Stack Interaction**: Pushed onto the stack as single units in their raw form
  3. **Delayed Execution**: Can be executed later when needed (via `eval`, `if`, `times`, etc.)

  **Common Use Cases:**
  - Conditional statements (`if`, `ifelse`)
  - Loop controls (`times`, `do`, `dolist`)
  - Function definitions (`defun`, `lambda`)
  - Lazy evaluation patterns

  **Examples:**
  ```bash
  # Create a code block
  stacker:0> {1 2 +}
  [{1 2 +}]

  # Execute with eval
  stacker:1> {1 2 +} eval
  [3]

  # Use in function definitions
  stacker:2> {x y} {x y *} multiply defun
  ```

  **Note**: Code blocks are stored but not executed until explicitly triggered. This allows for flexible program control, lazy evaluation, and higher-order programming patterns.

- ### Control Structures in Stacker

  Stacker provides two main types of control structures: conditionals and loops. These allow for dynamic program flow based on conditions and repetitive execution of code blocks.

  - #### Conditionals

    Conditionals in Stacker enable execution of code based on specified conditions.

  - ##### if Statement

    The `if` statement executes a code block if a condition is true.

    Syntax:
    ```bash
    condition <true-expr> if
    ```

    Example:
    ```bash
    stacker:0> 0 x set
    stacker:1> x 0 == {3 4 +} if
    [7]
    ```

    Result: Pushes `7` onto the stack as `x` equals `0`.

  - ##### ifelse Statement

    The `ifelse` statement provides branching based on a condition, executing one of two code blocks.

    Syntax:
    ```bash
    condition <true-expr> <false-expr> ifelse
    ```

    Example:
    ```bash
    stacker:0> 0 x set
    stacker:1> x 0 == {3 4 +} {3 4 -} ifelse
    [7]
    ```

    Result: Pushes `7` onto the stack as `x` equals `0`.

  - #### Loops

    Loops in Stacker allow for repeated execution of code blocks.

  - ##### do Loop

    The `do` loop iterates over a range of values.

    Syntax:
    ```bash
    start_value end_value symbol {body} do
    ```

    Example:
    ```bash
    stacker:0> 1 10 i {i echo} do
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    ```

    Result: Prints numbers from 1 to 10.

  - ##### dolist

      The `dolist` loop iterates over a list of values.

      Syntax:
      ```bash
      [value1 value2 ... valueN] symbol {body} dolist
      ```

      Example:
      ```bash
      stacker:0> [1 2 3 4 5] i {i echo} dolist
      1
      2
      3
      4
      5
      ```

      Result: Prints numbers 1 through 5.

      Note:
        When expressing a list of consecutive values, the concise notation value1 valueN `seq` can be used instead of `[value1 value2 ... valueN]` to efficiently describe a sequence with a constant step size.

  - ##### times

    The `times` loop repeats a code block a specified number of times.

    Syntax:
    ```bash
    {body} n times
    ```

    Example:
    ```bash
    stacker:0> 1 {dup ++} 10 times
    [1 2 3 4 5 6 7 8 9 10 11]
    ```

    Result: Pushes numbers 1 through 11 onto the stack by repeatedly duplicating and incrementing.

  - #### break
    - syntax:
      ```bash
      {break}
      ```
    - example:
      ```bash
      stacker:0> 0 i set
      stacker:1> 0 9 i {{break} i 5 == if i echo} do
      0
      1
      2
      3
      4
      5
      ```
      This example prints the numbers from 0 to 5. When `i` is equal to `5`, the loop is terminated by `break`.

- ### Define a function:
  - syntax:
    ```bash
    {arg1 arg2 ... argN} {body} name defun
    ```
  - example:
    ```bash
    stacker:0> {x y} {x y *} multiply defun
    stacker:1> 10 20 multiply
    [200]
    ```
    This defines a function named `multiply` that takes two arguments `x` and `y` and multiplies them together.

- ### Define a macro:
  - syntax:
    ```bash
    {body} name defmacro
    ```
  - example:
    ```bash
    stacker:0> {2 ^ 3 * 5 +} calculatePowerAndAdd defmacro
    stacker:1> 5 calculatePowerAndAdd
    [80]
    ```
    This defines a macro with the body `{2 ^ 3 * 5 +}` and assigns it the name `calculatePowerAndAdd`. This macro squares the number on the stack, multiplies it by 3, and then adds 5.

- ### Lambda Functions
  Lambda functions are anonymous functions that can be defined and executed on the fly. They are useful for creating temporary functions without the need for a formal definition.

  - syntax:
    ```bash
    {arg1 arg2 ... argN} {body} lambda
    ```
  - example:
    ```bash
    stacker:0> {x y} {x y *} lambda
    [λxλy.{x y *}]
    ```

  - example:
    ```bash
    stacker:0> {x y} {x y *} lambda multiply set
    stacker:1> 3 4 multiply
    [12]
    ```
    This example defines a lambda function that multiplies two numbers and assigns it to the variable `multiply`. The function is then called with the arguments `3` and `4`.


- ### Include Scripts
  Stacker scripts can be included in other scripts using the `include` command. For example:

  ``` bash
  stacker:0>  "my_script.stk" include
  ```
  All functions, macros and variables defined in "my_script.stk" are added to the current stack.


## Running Scripts
Stacker scripts can be created in `.stk` files. To run a script, simply execute it with Stacker. For example:

- my_script.stk:
  ```bash
  0 p set
  0 100000 k {
      -1 k ^ 2 k * 1 + / p + p set
  } do
  4 p * p set
  p echo
  ```

  Running the script:
  ```bash
  stacker my_script.stk
  ```


## VSCode Syntax Highlighting

Stacker provides syntax highlighting support for `.stk` files in Visual Studio Code, making it easier to read and write Stacker code.

### Installation

Install the syntax highlighting extension by copying it to your VSCode extensions directory:

```bash
# For VSCode Server (Remote SSH)
mkdir -p ~/.vscode-server/extensions/stacker-language-0.1.0
cp -r .vscode-extension/* ~/.vscode-server/extensions/stacker-language-0.1.0/

# For local VSCode
mkdir -p ~/.vscode/extensions/stacker-language-0.1.0
cp -r .vscode-extension/* ~/.vscode/extensions/stacker-language-0.1.0/
```

Then reload VSCode (Ctrl+Shift+P → "Developer: Reload Window").

### Features

- **Comment highlighting** (`#`) - Green, italic
- **String literals** (`"..."`, `'...'`) - Brown
- **Number literals** (`42`, `3.14`, `0xFF`, `0b1010`) - Light green
- **Operators** (`+`, `-`, `and`, `or`, etc.) - Blue
- **Control flow** (`if`, `do`, `times`) - Purple
- **Function definitions** (`defun`, `defmacro`, `lambda`) - Teal, bold
- **Variables** (`$x`, `a`) - Light blue
- **Assignment** (`set`, `=`, `global`) - White, bold
- Auto-closing brackets (`{`, `[`, `"`, `'`)
- Code folding support

For detailed installation instructions, see [VSCODE_SETUP.md](VSCODE_SETUP.md).


## Command Line Execution
You can directly execute a specified RPN expression from the command line.

```bash
stacker -e "3 4 + echo"
```


## Settings
- disable_plugin
  Disable a specified plugin:
  ```bash
  stacker:0> "hoge" disable_plugin
  ```
  This command deactivates the `hoge` operator added as a plugin.
  Note that it cannot be used on non-plugin operators.

- disable_all_plugins
  Disable all plugins at once.
  ```bash
  stacker:0> disable_all_plugins
  ```

- enable_disp_ans
  Enables the display of the last result (ans) at the end of the stack.
  ```bash
  stacker:0> enable_disp_ans
  stacker:1> 3 4 +
  7
  [7]
  ```

- disable_disp_ans
  Disables the display of the last result (ans) at the end of the stack.
  ```bash
  stacker:0> disable_disp_ans
  stacker:1> 3 4 +
  [7]
  ```

- enable_disp_stack
  Enables the setting to display the stack contents each time. By default, this setting is already active.
  ```bash
  stacker:0> enable_disp_stack
  ```

- disable_disp_stack
  Sets the display of stack contents to be disabled. When this setting is enabled, only the latest element of the stack is displayed.
  ```bash
  stacker:0> disable_disp_stack
  ```

- disable_disp_logo
  Disables the display of the logo at startup.
  ```bash
  stacker:0> disable_disp_logo
  ```



## Configuration File
You can automatically load settings at startup. The configuration file should be placed in ~/.stackerrc. For example, if you write the following contents in ~/.stackerrc, the disable_disp_logo and disable_disp_stack will be automatically activated at startup.
```bash
disable_disp_logo
disable_disp_stack
enable_disp_ans
```

## Creating Plugins

Create custom plugins for Stacker using Python:

1. **Creating the Plugin**:
 In the `plugins` directory, create a new Python file for your plugin (e.g., `my_plugin.py`). 

    ``` 
    stacker/
    │
    ├── stacker/
    │   ├── plugins/
    │   │   ├── my_plugin.py
    │   │   └── ...
    │   │
    │   ├── data/
    │   ├── stacker.py
    │   ├── test.py
    │   └── ...
    │
    └── ...
    ```

    Adding your plugin here and reinstalling Stacker will apply the plugin permanently.

2. **Defining Functions and Classes**:
   Define the necessary functions and classes in `my_plugin.py`.

3. **Defining the `setup` Function**:
   In `my_plugin.py`, define a `setup` function that takes `stacker` as its only argument.

4. **Registering Custom Commands and Parameters**:

    Within the `setup` function, use the `register_plugin` method of `stacker` to register custom commands. Additionally, you can also register custom parameters using the `register_parameter` method. This allows for greater flexibility and customization in your plugin's behavior.

    Here's an example where custom commands for matrix operations and a custom parameter are registered:

    Example:
    ```python
    from stacker.stacker import Stacker

    def function(a, b):
        # Do something

    def setup(stacker: Stacker):
        stacker.register_plugin("command", function)
    ```

    You can specify the command description for the help command using desc. This field is optional.

    This example demonstrates how to register functions for matrix operations and how to set a custom parameter within a plugin. The register_parameter method is used to add a custom parameter to the Stacker environment, allowing for additional customization and control within your plugin.

5. **Reinstalling Stacker**:
   Run the following command to reinstall Stacker:
    ```
    > python setup.py install
    ```

    **Note**: If you want to apply the plugin only temporarily, create a `plugins` directory in the directory where Stacker is executed and add your plugin there. The method for creating it is the same as described above. This method does not require reinstalling Stacker.


6. **Using the Plugin**:
   When Stacker is launched, the plugin will automatically be loaded, and the custom commands will be available for use.

7. **Disabling Plugins**:
Use operatorName disable_plugin to disable a specific plugin.<br>
Use disable_all_plugins to disable all plugins.<br>


## Running on Python
You can also run Stacker as a Python module. For example:
```python
from stacker import Stacker
stacker = Stacker()
print(stacker.eval("3 4 +"))
```

## Supported Operations

### Basic Operators

| Operator | Description                                           | Example                    |
|----------|-------------------------------------------------------|----------------------------|
| +        | Add                                                   | `3 5 +`                    |
| -        | Subtract                                              | `10 3 -`                   |
| *        | Multiply                                              | `4 6 *`                    |
| /        | Divide                                                | `12 4 /`                   |
| //       | Integer divide                                        | `7 2 //`                   |
| %        | Modulus                                               | `9 2 %`                    |
| ^        | Power                                                 | `3 2 ^`                    |
| ==       | Equal                                                 | `1 1 ==`                   |
| !=       | Not equal                                             | `1 0 !=`                   |
| <        | Less than                                             | `1 2 <`                    |
| <=       | Less than or equal to                                 | `3 3 <=`                   |
| >        | Greater than                                          | `2 1 >`                    |
| >=       | Greater than or equal to                              | `3 3 >=`                   |
| neg      | Negate                                                | `5 neg`                    |
| and      | Logical and                                           | `true false and`           |
| or       | Logical or                                            | `true false or`            |
| not      | Logical not                                           | `true not`                 |
| band     | Bitwise and                                           | `3 2 band`                 |
| bor      | Bitwise or                                            | `3 2 bor`                  |
| bxor     | Bitwise xor                                           | `3 2 bxor`                 |
| >>       | Right bit shit                                        | `8 2 >>`                   |
| <<       | Left bit shit                                         | `2 2 <<`                   |
| ~        | Bitwise not                                           | `5 ~`                      |
| bin      | Binary representation (result is a string)            | `5 bin`                    |
| oct      | Octal representation (result is a string)             | `10 oct`                   |
| dec      | Decimal representation (result is an integer)         | `0b101010 dec`             |
| hex      | Hexadecimal representation (result is a string)       | `255 hex`                  |


### Math Operator

| Operator | Description                                           | Example                    |
|----------|-------------------------------------------------------|----------------------------|
| abs      | Absolute value                                        | `-3 abs`                   |
| exp      | Exponential                                           | `3 exp`                    |
| log      | Natural logarithm                                     | `2 log`                    |
| log10    | Common logarithm (base 10)                            | `4 log10`                  |
| log2     | Logarithm base 2                                      | `4 log2`                   |
| sin      | Sine                                                  | `30 sin`                   |
| cos      | Cosine                                                | `45 cos`                   |
| tan      | Tangent                                               | `60 tan`                   |
| asin     | Arcsine                                               | `0.5 asin`                 |
| acos     | Arccosine                                             | `0.5 acos`                 |
| atan     | Arctangent                                            | `1 atan`                   |
| sinh     | Hyperbolic sine                                       | `1 sinh`                   |
| cosh     | Hyperbolic cosine                                     | `1 cosh`                   |
| tanh     | Hyperbolic tangent                                    | `1 tanh`                   |
| asinh    | Inverse hyperbolic sine                               | `1 asinh`                  |
| acosh    | Inverse hyperbolic cosine                             | `2 acosh`                  |
| atanh    | Inverse hyperbolic tangent                            | `0.5 atanh`                |
| sqrt     | Square root                                           | `9 sqrt`                   |
| ceil     | Ceiling                                               | `3.2 ceil`                 |
| floor    | Floor                                                 | `3.8 floor`                |
| round    | Round                                                 | `3.5 round`                |
| roundn   | Round to specified decimal places                     | `3.51 1 roundn`            |
| float    | Convert to floating-point number                      | `5 float`                  |
| int      | Convert to integer                                    | `3.14 int`                 |
| gcd      | Greatest common divisor                               | `4 2 gcd`                  |
| !        | Factorial                                             | `4 !`                      |
| radians  | Convert degrees to radians                            | `180 radians`              |
| random   | Generate a random floating-point number between 0 and 1| `random`                  |
| randint  | Generate a random integer within a specified range    | `1 6 randint`              |
| uniform  | Generate a random floating-point number within a specified range | `1 2 uniform`   |
| frac     | Fraction                                              | `3 6 frac`                 |
| dice     | Roll dice (e.g., 3d6)                                 | `3 6 dice`                 |


### Stack Operators
| Operator | Description                                               | Example                |
|----------|-----------------------------------------------------------|------------------------|
| drop     | Drops the top element of the stack.                       | `drop`                 |
| drop2    | Drops the top two elements of the stack.                  | `drop2`                |
| dropn    | Drops the nth element from the top of the stack.          | `n drop`               |
| dup      | Duplicate the top element of the stack.                   | `dup`                  |
| dup2     | Duplicate the top two elements of the stack.              | `dup2`                 |
| dupn     | Duplicate the nth element from the top of the stack.      | `n dup`                |
| swap     | Swap the top two elements of the stack.                   | `swap`                 |
| rev      | Reverse the stack.                                        | `rev`                  |
| rot      | Move the third element to the top of the stack.           | `rot`                  |
| unrot    | Move the top element to the third position of the stack.  | `unrot`                |
| roll     | Moves the nth element to the top of the stack.            | `roll`                 |
| over     | Copy the second element from the top of the stack.        | `over`                 |
| pick     | Copies the nth element to the top of the stack.           | `n pick`               |
| nip      | Remove the second element from the top of the stack.      | `nip`                  |
| depth    | Returns the depth of the stack.                           | `depth`                |
| ins      | Insert the specified value at the specified position.     | `3 1 ins`              |
| count    | Counts the number of occurrences of a value in the stack. | `count`                |
| clear    | Clear the stack.                                          | `clear`                |
| disp     | Display the stack.                                        | `disp`                 |


### Control Operators
| Operator | Description                                           | Example                    |
|----------|-------------------------------------------------------|----------------------------|
| if       | Conditional statement                                 | `{...} true  if`           |
| ifelse   | Conditional statement with an else block              | `{true block} {false block} true ifelse`  |
| iferror  | Conditional statement for error handling              | `{try block} {catch block} iferror` |
| do       | Loop                                                  | `0 10 i {i echo} do`      |
| times    | Loop a specified number of times                      | `{dup ++} 10 times`        |
| break    | Break out of a loop                                    | `break`                   |


### Function, Macro, Lambda, and Variable Operators
| Operator | Description                                           | Example                    |
|----------|-------------------------------------------------------|----------------------------|
| defun    | Define a function                                     | `{x y} {x y *} multiply defun` |
| defmacro    | Define a macro                                     | `{2 ^ 3 * 5 +} calculatePowerAndAdd defmacro` |
| lambda   | Create a lambda function                              | `{x y} {x y *} lambda`    |
| set      | Assign a value to a variable                          | `3 x set`                |
| =        | Assign a value to a variable (alias for `set`)        | `3 x =`                  |
| global   | Assign a value to a global variable                   | `42 $answer global`      |


### Array Operators
| Operator | Description                                           | Example                    |
|----------|-------------------------------------------------------|----------------------------|
| map      | Apply a function to each element of an array          | `[1 2 3] {dup} map`        |
| zip      | Combine two arrays into a single array                | `[1 2 3] [4 5 6] zip`      |
| filter   | Filter an array based on a condition                  | `[1 2 3 4 5] {2 % 0 ==} filter` |
| all      | Check if all elements of an array satisfy a condition  | `[1 2 3 4 5] {2 % 0 ==} all` |
| any      | Check if any element of an array satisfies a condition | `[1 2 3 4 5] {2 % 0 ==} any` |


### Other Operators
| Operator | Description                                           | Example                    |
|----------|-------------------------------------------------------|----------------------------|
| sub      | Substack the top element of the stack                 | `sub`                      |
| subn     | Cluster elements between the top and the nth (make substacks) | `3 subn`           |
| include  | Include the specified file                            | `"file.stk" include`       |
| eval     | Evaluate the specified RPN expression                 | `'3 5 +' eval`             |
| echo     | Print the specified value to stdout without adding it to the stack | `3 4 + echo`  |
| input    | Get input from the user                               | `input`                    |
| read     | Reads a string from the console                       | `read`                     |
| write-to-file | Write the top element of the stack to a file       | `3 "output.txt" write-to-file` |
| append-to-file | Append the top element of the stack to a file      | `3 "output.txt" append-to-file` |
| read-from-file | Read the contents of a file and push it to the stack | `"input.txt" read-from-file` |
| file-exists | Check if a file exists                                | `"file.txt" file-exists`    |



## Constants
| Constants | Description      |
|-----------|------------------|
| e         | Euler's number   |
| pi        | Pi               |
| tau       | Tau              |
| nan       | Not a number     |
| inf       | Infinity         |
| true      | Boolean true     |
| false     | Boolean false    |

--- stacker/examples/README.md ---
# Stacker Examples

This directory contains example programs demonstrating various features of the Stacker language.

## Directory Structure

### basics/
Fundamental language features and control structures:
- **variables.stk** - Variable assignment, scope, and global variables
- **stack_operations.stk** - Stack manipulation (dup, swap, rot, etc.)
- **conditionals.stk** - Conditional statements (if, ifelse) and comparisons
- **types.stk** - Data types and type conversions
- **fizzbuzz.stk** - Classic FizzBuzz problem
- **loops.stk** - Nested loop examples
- **error_handling.stk** - Error handling with `iferror`
- **break.stk** - Breaking out of loops

### functions/
Function and macro definitions:
- **function_basics.stk** - Basic function definition and usage
- **function_and_macro.stk** - Difference between functions and macros
- **lambda.stk** - Lambda functions and closures
- **recursion.stk** - Recursive functions and patterns
- **higher_order.stk** - Higher-order functions (map, filter, reduce)

### algorithms/
Classic algorithms and computational examples:
- **factorial.stk** - Recursive factorial calculation
- **fibonacci.stk** - Iterative Fibonacci calculation
- **gcd.stk** - Euclidean algorithm for GCD
- **square_sum.stk** - Sum of squares calculation
- **pi_calculation.stk** - Pi approximation using Leibniz formula
- **sorting.stk** - Sorting algorithms (bubble, selection, insertion, merge, quick)
- **prime_numbers.stk** - Prime number detection and generation

### advanced/
Advanced features and patterns:
- **global_variables.stk** - Using global variables
- **string_operations.stk** - String manipulation and processing
- **file_io.stk** - File operations (read, write, append)
- **eval_examples.stk** - Dynamic code execution with eval

## Running Examples

Run any example with:
```bash
stacker examples/basics/fizzbuzz.stk
```

Or explore them interactively:
```bash
stacker
stacker:0> "examples/basics/fizzbuzz.stk" include
```

## Syntax Notes

All examples use the modern Stacker syntax:
- Variable assignment: `value variable =` (not `value $variable =`)
- Variable reference: `variable` (not `$variable`)
- The `$` prefix is supported for backward compatibility but not recommended


--- stacker/examples/algorithms/factorial.stk ---
# Factorial calculation using recursion

{n} {
    n 1 <=
    {1}
    {n n 1 - fact *}
    ifelse
} fact defun

# Calculate 5!
5 fact echo  # Output: 120


--- stacker/examples/algorithms/prime_numbers.stk ---
# Prime Numbers - Detection and generation

# ===== Prime Check (Basic) =====
"=== Prime Check (Basic) ===" echo

{n} {
    n 2 < {
        false
    } {
        n 2 == {
            true
        } {
            true is_prime =
            2 n sqrt int 1 + i {
                n i % 0 == {
                    false is_prime =
                } if
            } do
            is_prime
        } ifelse
    } ifelse
} is_prime defun

"Is 2 prime?" echo
2 is_prime echo
"Is 17 prime?" echo
17 is_prime echo
"Is 20 prime?" echo
20 is_prime echo
"Is 97 prime?" echo
97 is_prime echo

# ===== Prime Check (Optimized) =====
"" echo
"=== Prime Check (Optimized) ===" echo

{n} {
    n 2 < {
        false
    } {
        n 2 == n 3 == or {
            true
        } {
            n 2 % 0 == n 3 % 0 == or {
                false
            } {
                true is_prime =
                5 i =
                {i i * n <= is_prime and} {
                    n i % 0 == n i 2 + % 0 == or {
                        false is_prime =
                    } if
                    i 6 + i =
                } while
                is_prime
            } ifelse
        } ifelse
    } ifelse
} is_prime_fast defun

"Is 97 prime (fast)?" echo
97 is_prime_fast echo
"Is 100 prime (fast)?" echo
100 is_prime_fast echo

# ===== Count primes up to N =====
"" echo
"=== Count Primes up to N ===" echo

{n} {
    0 count =
    2 n i {
        i is_prime {
            count 1 + count =
        } if
    } do
    count
} count_primes defun

"Number of primes up to 100:" echo
100 count_primes echo

# ===== Next Prime =====
"" echo
"=== Next Prime ===" echo

{n} {
    n 1 + candidate =
    true searching =
    {searching} {
        candidate is_prime {
            false searching =
        } {
            candidate 1 + candidate =
        } ifelse
    } while
    candidate
} next_prime defun

"Next prime after 10:" echo
10 next_prime echo
"Next prime after 20:" echo
20 next_prime echo

# ===== Prime Factorization (Demonstration) =====
"" echo
"=== Prime Factorization ===" echo

"60 = 2 * 2 * 3 * 5" echo
"84 = 2 * 2 * 3 * 7" echo
"17 = 17 (prime)" echo
"" echo
"Note: Full factorization requires list operations" echo

# ===== Info =====
"" echo
"=== Info ===" echo
"Prime numbers are fundamental in number theory" echo
"They are used in cryptography, hashing, and more" echo
"" echo
"Note: Advanced prime algorithms (sieve, twin primes) require" echo
"      list mutation operators (append, put) which are" echo
"      currently not available in this version of Stacker." echo


--- stacker/examples/algorithms/square_sum.stk ---
# Sum of squares from 1 to 100

0 s =
1 100 i {
    s i 2 ^ + s =
} do

"Result: " s str + echo  # Output: Result: 338350


--- stacker/examples/algorithms/sorting.stk ---
# Sorting Algorithms

# ===== Built-in Sort =====
"=== Built-in Sort ===" echo

"Sorted:" echo
[5 2 8 1 9] sorted echo
"Float sort:" echo
[3.5 1.2 9.8 2.1] sorted echo

# ===== Reverse =====
"" echo
"=== Reverse ===" echo

"Reversed:" echo
[1 2 3 4 5] rev echo

# ===== Comparing sorted vs original =====
"" echo
"=== Comparing Lists ===" echo

"Is [1,2,3,4,5] sorted?" echo
[1 2 3 4 5] dup sorted == echo
"Is [1,3,2,4] sorted?" echo
[1 3 2 4] dup sorted == echo

# ===== Performance Comparison Info =====
"" echo
"=== Sorting Algorithm Complexity ===" echo
"Built-in sorted: O(n log n) - Optimized implementation" echo
"" echo
"Note: Advanced sorting algorithms (bubble, merge, quick) require" echo
"      list mutation operators (put, slice, append) which are" echo
"      currently not available in this version of Stacker." echo
"      Use the built-in 'sorted' operator for sorting needs." echo


--- stacker/examples/algorithms/pi_calculation.stk ---
# Calculate pi using Leibniz formula: π/4 = 1 - 1/3 + 1/5 - 1/7 + ...

0 p =
0 100000 k {
    -1 k ^ 2 k * 1 + / p + p =
} do
4 p * p =

"Pi approximation: " p str + echo


--- stacker/examples/algorithms/fibonacci.stk ---
# Fibonacci calculation using iteration

{n} {
    n 0 == {0} {
        n 1 == {1} {
            0 a =
            1 b =
            2 n i {
                a b + temp =
                b a =
                temp b =
            } do
            b
        } ifelse
    } ifelse
} fib defun

# Calculate 10th Fibonacci number
10 fib echo  # Output: 55


--- stacker/examples/algorithms/gcd.stk ---
# Greatest Common Divisor using Euclidean algorithm

{a b} {
    b 0 ==
    {a}
    {b a b % gcd}
    ifelse
} gcd defun

# Calculate GCD of 48 and 18
48 18 gcd echo  # Output: 6


--- stacker/examples/basics/types.stk ---
# Data Types - Exploring different data types in Stacker

# ===== Integers =====
"=== Integers ===" echo

42 echo
-17 echo
0 echo

# Arithmetic
10 3 + "10 + 3 =" swap echo
10 3 - "10 - 3 =" swap echo
10 3 * "10 * 3 =" swap echo
10 3 / "10 / 3 =" swap echo
10 3 % "10 % 3 =" swap echo

# ===== Floating Point Numbers =====
"" echo
"=== Floating Point Numbers ===" echo

3.14 echo
-2.5 echo
0.0 echo

# Arithmetic with floats
3.14 2.0 * "3.14 * 2.0 =" swap echo

# Power
2.0 3.0 ^ "2.0 ^ 3.0 =" swap echo

# ===== Different Number Bases =====
"" echo
"=== Number Bases ===" echo

# Binary (0b prefix)
0b1010 "Binary 0b1010 =" swap echo  # 10 in decimal

# Octal (0o prefix)
0o17 "Octal 0o17 =" swap echo  # 15 in decimal

# Hexadecimal (0x prefix)
0xFF "Hex 0xFF =" swap echo  # 255 in decimal

# ===== Complex Numbers =====
"" echo
"=== Complex Numbers ===" echo

# Complex number: real+imagj
3+4j "Complex number:" swap echo

# Complex arithmetic
1+2j 3+4j + "1+2j + 3+4j =" swap echo

# ===== Strings =====
"" echo
"=== Strings ===" echo

"Hello, World!" echo
"Stacker" echo

# String concatenation
"Hello" " " + "World!" + echo

# String conversion
42 str "Number as string:" swap echo
3.14 str "Float as string:" swap echo

# ===== Booleans =====
"" echo
"=== Booleans ===" echo

true echo
false echo

# Boolean operations
true false and "true AND false =" swap echo
true false or "true OR false =" swap echo
true not "NOT true =" swap echo

# ===== Lists =====
"" echo
"=== Lists ===" echo

[1 2 3 4 5] "List:" swap echo

# List operations
[1 2 3] len "Length of [1 2 3]:" swap echo

[3 1 2] sorted "Sorted [3 1 2]:" swap echo

[1 2 3] rev "Reversed [1 2 3]:" swap echo

# Creating list from stack
1 2 3 4 5 5 listn "List from 5 elements:" swap echo

# ===== Fractions =====
"" echo
"=== Fractions ===" echo

3 4 frac "Fraction 3/4:" swap echo

1 2 frac 1 3 frac + "1/2 + 1/3 =" swap echo

# ===== Special Values =====
"" echo
"=== Special Values ===" echo

pi "Pi:" swap echo
e "Euler's number:" swap echo
tau "Tau (2*pi):" swap echo
inf "Infinity:" swap echo
nan "Not a Number:" swap echo

# ===== Type Checking =====
"" echo
"=== Type Checking ===" echo

42 type "Type of 42:" swap echo
3.14 type "Type of 3.14:" swap echo
"hello" type "Type of 'hello':" swap echo
true type "Type of true:" swap echo
[1 2 3] type "Type of [1 2 3]:" swap echo
3+4j type "Type of 3+4j:" swap echo

# ===== Type Conversion =====
"" echo
"=== Type Conversion ===" echo

# To integer
3.7 int "3.7 to int:" swap echo
"42" int "\"42\" to int:" swap echo

# To float
42 float "42 to float:" swap echo

# To string
123 str "123 to string:" swap echo

# To binary, octal, hex
255 bin "255 to binary:" swap echo
255 oct "255 to octal:" swap echo
255 hex "255 to hex:" swap echo

# ===== Code Blocks =====
"" echo
"=== Code Blocks ===" echo

{1 2 +} "Code block:" swap echo
{1 2 +} type "Type of code block:" swap echo

# Evaluating code block
{5 3 *} eval "Evaluated {5 3 *}:" swap echo


--- stacker/examples/basics/variables.stk ---
# Variables - Basic usage and scope

# ===== Variable Assignment =====
"=== Variable Assignment ===" echo

# Using = operator (modern syntax)
42 answer =
"The answer is:" answer str + echo

# Using set operator (traditional syntax)
3.14 pi set
"Pi is approximately:" pi str + echo

# Multiple assignments
10 x =
20 y =
"x + y =" x y + str + echo

# ===== Variable Scope =====
"" echo
"=== Variable Scope ===" echo

# Local scope in functions
100 outer =

{x} {
    x 2 * inner =  # inner is local to this function
    "Inside function - inner:" inner str + echo
    "Inside function - outer:" outer str + echo  # Can access outer scope
    inner  # Return value
} test_scope defun

50 test_scope result =

# inner is not accessible here (local to function)
"After function - outer:" outer str + echo
"Function returned:" result str + echo

# ===== Global Variables =====
"" echo
"=== Global Variables ===" echo

0 counter global

{x} {
    counter 1 + counter =  # Increment global counter
    x counter *
} multiply_by_counter defun

# Each call increments the counter
5 multiply_by_counter "Counter=1:" swap echo
5 multiply_by_counter "Counter=2:" swap echo
5 multiply_by_counter "Counter=3:" swap echo

# ===== Variable Names =====
"" echo
"=== Variable Names ===" echo

# Variables can have descriptive names
100 user_score =
"Alice" user_name =

"User:" user_name str + echo
"Score:" user_score str + echo

# ===== Old Syntax (backward compatibility) =====
"" echo
"=== Old Syntax (still works) ===" echo

# Using set operator (old style)
123 old_var set
old_var echo

# Modern style with = operator (recommended)
456 new_var =
new_var echo


--- stacker/examples/basics/error_handling.stk ---
# Error handling with 'iferror'

# Example 1: Catch an error
{undefined_symbol} {"Error caught!" echo} iferror

# Example 2: No error occurs
{0 x = x echo} {"This won't be executed" echo} iferror


--- stacker/examples/basics/conditionals.stk ---
# Conditionals - if and ifelse statements

# ===== Basic if Statement =====
"=== Basic if Statement ===" echo

# Syntax: condition {true-block} if
true {"This is true!" echo} if

false {"This won't print" echo} if

# ===== Numeric Comparisons =====
"" echo
"=== Numeric Comparisons ===" echo

10 5 > {"10 is greater than 5" echo} if

3 7 < {"3 is less than 7" echo} if

5 5 == {"5 equals 5" echo} if

4 4 >= {"4 is greater than or equal to 4" echo} if

# ===== ifelse Statement =====
"" echo
"=== ifelse Statement ===" echo

# Syntax: condition {true-block} {false-block} ifelse

18 age =
age 18 >= {
    "You are an adult" echo
} {
    "You are a minor" echo
} ifelse

# ===== Nested Conditionals =====
"" echo
"=== Nested Conditionals ===" echo

85 score =

score 90 >= {
    "Grade: A" echo
} {
    score 80 >= {
        "Grade: B" echo
    } {
        score 70 >= {
            "Grade: C" echo
        } {
            "Grade: D or F" echo
        } ifelse
    } ifelse
} ifelse

# ===== Logical Operations =====
"" echo
"=== Logical Operations ===" echo

# and operator
true true and {"Both true" echo} if

true false and {"Won't print (and with false)" echo} if

# or operator
true false or {"At least one true" echo} if

false false or {"Won't print (both false)" echo} if

# not operator
false not {"Not false = true" echo} if

# ===== Complex Conditions =====
"" echo
"=== Complex Conditions ===" echo

15 x =
10 y =

# Check if x is between 10 and 20
x 10 >= x 20 <= and {
    "x is between 10 and 20" echo
} if

# Check if either x or y is greater than 12
x 12 > y 12 > or {
    "At least one value is greater than 12" echo
} if

# ===== Conditional Assignment =====
"" echo
"=== Conditional Assignment ===" echo

-5 num =

# Get absolute value
num 0 < {
    num -1 *
} {
    num
} ifelse abs_value =

"Absolute value of -5:" abs_value str + echo

# ===== Using Conditionals in Functions =====
"" echo
"=== Conditionals in Functions ===" echo

# Max function
{a b} {
    a b > {a} {b} ifelse
} max defun

5 3 max "Max of 5 and 3:" swap echo

# Sign function
{n} {
    n 0 > {
        1
    } {
        n 0 < {
            -1
        } {
            0
        } ifelse
    } ifelse
} sign defun

-7 sign "Sign of -7:" swap echo
0 sign "Sign of 0:" swap echo
42 sign "Sign of 42:" swap echo

# ===== Even/Odd Check =====
"" echo
"=== Even/Odd Check ===" echo

{n} {
    n 2 % 0 == {
        "even"
    } {
        "odd"
    } ifelse
} even_or_odd defun

7 even_or_odd "7 is" swap + echo
12 even_or_odd "12 is" swap + echo


--- stacker/examples/basics/break.stk ---
# Breaking out of a loop

0 100 i {
    i echo
    i 6 == {break} if
} do


--- stacker/examples/basics/loops.stk ---
# Nested loop example using 'do'

0 1 i {
    "i: " i str + echo
    3 4 j {
        "  j: " j str + echo
        5 6 k {
            "    k: " k str + echo
        } do
    } do
} do


--- stacker/examples/basics/fizzbuzz.stk ---
# FizzBuzz: Print numbers 1-100, replacing multiples of 3 with "fizz",
# multiples of 5 with "buzz", and multiples of both with "fizzbuzz"

1 100 i {
    i 3 % 0 == i 5 % 0 == and
    {"fizzbuzz" echo}
    {
        i 5 % 0 ==
        {"buzz" echo}
        {
            i 3 % 0 ==
            {"fizz" echo}
            {i echo}
            ifelse
        }
        ifelse
    }
    ifelse
} do


--- stacker/examples/basics/stack_operations.stk ---
# Stack Operations - Fundamental stack manipulation

# ===== Basic Stack Operations =====
"=== Basic Stack Operations ===" echo

# dup - Duplicate top element
5 dup
"After '5 dup':" echo echo  # Prints 5 twice

# swap - Swap top two elements
10 20 swap
"After '10 20 swap':" echo echo  # Prints 10, then 20

# drop - Remove top element
1 2 3 drop
"After '1 2 3 drop':" echo echo  # Prints 2, then 1

# ===== Rotation Operations =====
"" echo
"=== Rotation Operations ===" echo

# rot - Rotate top 3 elements (a b c -> b c a)
1 2 3 rot
"After '1 2 3 rot':" echo echo echo  # Prints 1, 3, 2

# unrot - Rotate top 3 elements in reverse (a b c -> c a b)
1 2 3 unrot
"After '1 2 3 unrot':" echo echo echo  # Prints 2, 1, 3

# ===== Stack Inspection =====
"" echo
"=== Stack Inspection ===" echo

# depth - Get stack depth
1 2 3
"Stack depth:" depth str + echo
drop drop drop

# clear - Clear the stack
1 2 3 4 5
"Before clear, depth:" depth str + echo
clear
"After clear, depth:" depth str + echo

# ===== Over Operation =====
"" echo
"=== Over Operation ===" echo

# over - Copy second element to top
10 20 over
"After '10 20 over':" echo echo echo  # Prints 10, 20, 10

# ===== Multiple Duplication =====
"" echo
"=== Multiple Duplication ===" echo

# dupn - Duplicate top n elements
1 2 3 3 dupn
"After '1 2 3 3 dupn' (depth):" depth str + echo
clear

# ===== List Operations =====
"" echo
"=== List Operations ===" echo

# listn - Create list from top n elements
1 2 3 4 5 3 listn
"List from top 3 elements:" echo
drop drop

# ===== Practical Examples =====
"" echo
"=== Practical Examples ===" echo

# Example 1: Compute (a+b) and (a-b) without losing a and b
5 a =
3 b =

a b      # Stack: 5 3
2 dupn   # Stack: 5 3 5 3
+        # Stack: 5 3 8
swap     # Stack: 5 8 3
rot      # Stack: 8 3 5
swap     # Stack: 8 5 3
-        # Stack: 8 2

"Sum:" swap echo
"Difference:" echo

# Example 2: Average of three numbers
10 20 30
3 dupn    # Duplicate all three
+ +       # Sum them
3 /       # Divide by 3
"Average of 10, 20, 30:" echo


--- stacker/examples/functions/lambda.stk ---
# Lambda Functions - Anonymous functions

# ===== Basic Lambda =====
"=== Basic Lambda ===" echo

# Syntax: {params} {body} lambda
# Creates an anonymous function

{x} {x 2 *} lambda "Lambda function created" drop echo

# Using lambda immediately
5 {x} {x 2 *} lambda "5 * 2 =" swap echo

# ===== Storing Lambda in Variable =====
"" echo
"=== Storing Lambda in Variable ===" echo

{x} {x 2 *} lambda double =

10 double "10 * 2 =" swap echo
7 double "7 * 2 =" swap echo

# ===== Multiple Parameters =====
"" echo
"=== Multiple Parameters ===" echo

{x y} {x y +} lambda add =

5 3 add "5 + 3 =" swap echo

{a b c} {a b * c +} lambda calc =

2 3 4 calc "2 * 3 + 4 =" swap echo

# ===== Lambda vs defun =====
"" echo
"=== Lambda vs defun ===" echo

# Using defun (named function)
{x} {x x *} square defun
5 square "5^2 (defun) =" swap echo

# Using lambda (anonymous function)
{x} {x x *} lambda square_lambda =
5 square_lambda "5^2 (lambda) =" swap echo

# ===== Lambda in Higher-Order Functions =====
"" echo
"=== Lambda with map ===" echo

# map with code block (not lambda)
# map uses code blocks where the element is on the stack
[1 2 3 4 5] {2 *} map echo

# Square each element
[1 2 3 4] {dup *} map "Squares:" swap echo

# ===== Lambda with filter =====
"" echo
"=== Lambda with filter ===" echo

# Filter even numbers
[1 2 3 4 5 6 7 8] {2 % 0 ==} filter echo

# Filter numbers > 5
[1 3 5 7 9 11] {5 >} filter "Numbers > 5:" swap echo

# ===== Nested Lambdas =====
"" echo
"=== Nested Lambdas ===" echo

# Lambda that returns another lambda
{x} {
    {y} {x y +} lambda
} lambda make_adder =

5 make_adder add5 =

10 add5 "10 + 5 =" swap echo
7 add5 "7 + 5 =" swap echo

# ===== Lambda with Closures =====
"" echo
"=== Lambda with Closures ===" echo

# Counter using closure
{start} {
    {x} {start x +} lambda
} lambda make_counter =

100 make_counter counter =

5 counter "100 + 5 =" swap echo
10 counter "100 + 10 =" swap echo

# ===== Practical Examples =====
"" echo
"=== Practical Examples ===" echo

# Example 1: Temperature converter
{celsius} {celsius 9 * 5 / 32 +} lambda celsius_to_fahrenheit =

0 celsius_to_fahrenheit "0°C =" swap echo "°F" echo
100 celsius_to_fahrenheit "100°C =" swap echo "°F" echo

# Example 2: Discount calculator
{price discount_pct} {
    price discount_pct 100 / * price swap -
} lambda apply_discount =

100 20 apply_discount "$100 with 20% discount: $" swap str + echo

# Example 3: Custom comparator
{threshold} {
    {x} {x threshold >} lambda
} lambda make_threshold_check =

10 make_threshold_check above_10 =

5 above_10 "Is 5 > 10?" swap echo
15 above_10 "Is 15 > 10?" swap echo


--- stacker/examples/functions/recursion.stk ---
# Recursion - Recursive function examples

# ===== Basic Recursion - Countdown =====
"=== Basic Recursion - Countdown ===" echo

{n} {
    n 0 > {
        n echo
        n 1 - countdown drop
    } if
    0  # Always return something (dummy value)
} countdown defun

5 countdown drop

# ===== Factorial (already in algorithms/, but shown here) =====
"" echo
"=== Factorial ===" echo

{n} {
    n 1 <= {
        1
    } {
        n n 1 - factorial *
    } ifelse
} factorial defun

5 factorial "5! =" swap echo
10 factorial "10! =" swap echo

# ===== Fibonacci (recursive version) =====
"" echo
"=== Fibonacci (Recursive) ===" echo

{n} {
    n 1 <= {
        n
    } {
        n 1 - fib_rec
        n 2 - fib_rec
        +
    } ifelse
} fib_rec defun

0 fib_rec "fib(0) =" swap echo
1 fib_rec "fib(1) =" swap echo
5 fib_rec "fib(5) =" swap echo
10 fib_rec "fib(10) =" swap echo

# Note: Recursive Fibonacci is inefficient for large n

# ===== Sum of List =====
"" echo
"=== Sum of List (Recursive) ===" echo

# Use reduce instead since we don't have tail/rest operations
[1 2 3 4 5] 0 acc x {acc x +} reduce "Sum of [1,2,3,4,5] =" swap echo

# ===== Power Function =====
"" echo
"=== Power (Recursive) ===" echo

{base exp} {
    exp 0 == {
        1
    } {
        base base exp 1 - power_rec *
    } ifelse
} power_rec defun

2 5 power_rec "2^5 =" swap echo
3 4 power_rec "3^4 =" swap echo

# ===== Greatest Common Divisor (Euclidean Algorithm) =====
"" echo
"=== GCD (Recursive Euclidean Algorithm) ===" echo

{a b} {
    b 0 == {
        a
    } {
        b a b % gcd_rec
    } ifelse
} gcd_rec defun

48 18 gcd_rec "GCD(48, 18) =" swap echo
100 35 gcd_rec "GCD(100, 35) =" swap echo

# ===== Binary Search (Recursive) =====
"" echo
"=== Binary Search (Recursive) ===" echo

# Helper function for binary search
{lst target low high} {
    low high > {
        -1  # Not found
    } {
        low high + 2 / int mid =
        lst mid nth mid_val =

        mid_val target == {
            mid
        } {
            mid_val target < {
                lst target mid 1 + high binary_search_helper
            } {
                lst target low mid 1 - binary_search_helper
            } ifelse
        } ifelse
    } ifelse
} binary_search_helper defun

# Main binary search function
{lst target} {
    lst target 0 lst len 1 - binary_search_helper
} binary_search defun

[1 3 5 7 9 11 13 15] 7 binary_search "Index of 7:" swap echo
[1 3 5 7 9 11 13 15] 13 binary_search "Index of 13:" swap echo
[1 3 5 7 9 11 13 15] 4 binary_search "Index of 4 (not found):" swap echo

# ===== Tower of Hanoi =====
"" echo
"=== Tower of Hanoi ===" echo

{n from to aux} {
    n 1 == {
        "Move disk from" from str + " to" + to str + echo
    } {
        n 1 - from aux to hanoi drop
        "Move disk from" from str + " to" + to str + echo
        n 1 - aux to from hanoi drop
    } ifelse
    0  # Return dummy value
} hanoi defun

"Solving Tower of Hanoi with 3 disks:" echo
3 "A" "C" "B" hanoi drop

# Note: String slicing operations are not available in this version
# so string reversal example is omitted

# ===== Tail Recursion Example =====
"" echo
"=== Tail Recursion - Factorial ===" echo

# Tail-recursive factorial (accumulator pattern)
{n acc} {
    n 1 <= {
        acc
    } {
        n 1 - n acc * factorial_tail
    } ifelse
} factorial_tail defun

{n} {
    n 1 factorial_tail
} factorial_tr defun

5 factorial_tr "5! (tail recursive) =" swap echo


--- stacker/examples/functions/higher_order.stk ---
# Higher-Order Functions - map, filter, reduce

# ===== map - Transform each element =====
"=== map - Transform Each Element ===" echo

# Syntax: list {body} map
# The element is implicitly on the stack in the body

# Double each element
[1 2 3 4 5] {2 *} map echo

# Square each element
[1 2 3 4] {dup *} map "Squares:" swap echo

# Add 10 to each element
[5 10 15] {10 +} map "Add 10:" swap echo

# ===== filter - Select elements =====
"" echo
"=== filter - Select Elements ===" echo

# Syntax: list var {condition} filter

# Filter even numbers
[1 2 3 4 5 6 7 8 9 10] {2 % 0 ==} filter echo

# Filter numbers greater than 5
[1 3 5 7 9 11] {5 >} filter "> 5:" swap echo

# Filter positive numbers
[-5 -2 0 3 7 -1 4] {0 >} filter "Positive:" swap echo

# ===== Combining map and filter =====
"" echo
"=== Combining map and filter ===" echo

# Get squares of even numbers
[1 2 3 4 5 6 7 8] {2 % 0 ==} filter
                   {dup *} map
"Squares of evens:" swap echo

# Double numbers greater than 3
[1 2 3 4 5 6] {3 >} filter
              {2 *} map
"Double of (>3):" swap echo

# ===== map with multiple operations =====
"" echo
"=== map with Complex Operations ===" echo

# Convert Celsius to Fahrenheit
[0 10 20 30 100] {9 * 5 / 32 +} map "°F:" swap echo

# Calculate areas of circles (A = πr²)
[1 2 3 4 5] {dup * pi *} map "Areas:" swap echo

# ===== filter with complex conditions =====
"" echo
"=== filter with Complex Conditions ===" echo

# Numbers divisible by 3
[1 2 3 4 5 6 7 8 9 10 11 12] {3 % 0 ==} filter "Div by 3:" swap echo

# Numbers in range [5, 10]
[1 3 5 7 9 11 13] {dup 5 >= swap 10 <= and} filter "In [5,10]:" swap echo

# ===== Nested lists with map =====
"" echo
"=== Nested Lists with map ===" echo

# Double all elements in nested lists
[[1 2] [3 4] [5 6]] {{2 *} map} map echo

# ===== Using map/filter with strings =====
"" echo
"=== map/filter with Strings ===" echo

# Not directly supported, but can work with character codes
# Example: Filter characters (conceptual)

# ===== Practical Examples =====
"" echo
"=== Practical Examples ===" echo

# Example 1: Calculate total price with tax
[10.0 20.0 30.0] {1.1 *} map "With 10% tax:" swap echo

# Example 2: Find perfect squares up to 100
[1 2 3 4 5 6 7 8 9 10] {dup *} map "Perfect squares:" swap echo

# Example 3: Get passing scores
[45 67 82 55 90 73] {60 >=} filter "Passing scores:" swap echo

# ===== Custom higher-order function =====
"" echo
"=== Custom Higher-Order Function ===" echo

# apply_twice - Apply function twice to a value
{val func} {
    val func
    func
} apply_twice defun

# Use it
10 {x} {x 2 *} lambda apply_twice "10 * 2 * 2 =" swap echo

5 {x} {x 1 +} lambda apply_twice "5 + 1 + 1 =" swap echo

# ===== Function composition =====
"" echo
"=== Function Composition ===" echo

# compose - Apply two functions in sequence
{x f g} {
    x f g
} compose defun

10 {x} {x 2 *} lambda {x} {x 5 +} lambda compose
"(10 * 2) + 5 =" swap echo

# ===== map with index =====
"" echo
"=== Simulating map with index ===" echo

# enumerate-like behavior using global counter
0 idx global

[10 20 30] val {
    "Index" idx str + ":" + val str + echo
    idx 1 + idx =
} dolist

# Reset counter
0 idx global


--- stacker/examples/functions/function_basics.stk ---
# Basic function definition and usage

# Define a function that multiplies two numbers
{x y} {x y *} multiply defun

# Use the function
3 4 multiply echo  # Output: 12


--- stacker/examples/functions/function_and_macro.stk ---
# Demonstrating the difference between functions and macros

# Function: evaluated at call time with arguments
{x y} {x y +} add defun

# Macro: code substitution at parse time
{2 ^ 3 * 5 +} square_times_3_plus_5 defmacro

# Using the function
10 20 add echo  # Output: 30

# Using the macro
5 square_times_3_plus_5 echo  # Output: 80 (5^2 * 3 + 5)


--- stacker/examples/advanced/global_variables.stk ---
# Global variables example

0 counter global

{x} {
    counter 1 + counter =  # Increment global counter
    x counter *
} multiply_by_counter defun

# Each call increments the counter
5 multiply_by_counter echo   # Output: 5  (5 * 1)
5 multiply_by_counter echo   # Output: 10 (5 * 2)
5 multiply_by_counter echo   # Output: 15 (5 * 3)


--- stacker/examples/advanced/file_io.stk ---
# File I/O - File operations

# ===== Writing to a File =====
"=== Writing to a File ===" echo

"This is a test file.
It has multiple lines.
Line 3 here." "test_output.txt" write-to-file

"File written to test_output.txt" echo

# ===== Reading from a File =====
"" echo
"=== Reading from a File ===" echo

"test_output.txt" read-from-file
"File contents:" echo
echo

# ===== Appending to a File =====
"" echo
"=== Appending to a File ===" echo

"
This line was appended." "test_output.txt" append-to-file

"Appended to file" echo

"test_output.txt" read-from-file
"Updated contents:" echo
echo

# ===== Check if File Exists =====
"" echo
"=== Check if File Exists ===" echo

"Does test_output.txt exist?" echo
"test_output.txt" file-exists echo

"Does nonexistent.txt exist?" echo
"nonexistent.txt" file-exists echo

# ===== Writing Multiple Lines =====
"" echo
"=== Writing Multiple Lines ===" echo

# Create a multi-line string
"Line 1
Line 2
Line 3
Line 4
Line 5" "multiline.txt" write-to-file

"Written multiline file" echo

# ===== Reading Lines =====
"" echo
"=== Reading Lines ===" echo

"multiline.txt" read-lines lines =

"Number of lines:" echo
lines len echo

# Print each line with line number
0 idx =
lines line {
    idx 1 + idx =
    idx str ":" + line + echo
} dolist

# ===== Writing Structured Data =====
"" echo
"=== Writing Structured Data ===" echo

# Write CSV-like data
"Name,Age,City
Alice,30,Tokyo
Bob,25,Osaka
Charlie,35,Kyoto" "data.csv" write-to-file

"CSV file written" echo

# ===== Writing Numbers to File =====
"" echo
"=== Writing Numbers to File ===" echo

# Generate and save numbers
"" content =
1 10 i {
    content i str + "\n" + content =
} do

content "numbers.txt" write-to-file
"Numbers written to file" echo

# ===== Logging Example =====
"" echo
"=== Logging Example ===" echo

{message} {
    "[LOG] " message + "\n" + "app.log" append-to-file
} log defun

"Application started" log
"Processing data" log
"Task completed" log

"app.log" read-from-file
"Log contents:" echo
echo

# ===== File-based Configuration =====
"" echo
"=== Configuration File ===" echo

"# Configuration file
timeout=30
max_retries=3
debug=true" "config.txt" write-to-file

"Configuration written" echo

"config.txt" read-lines
line {
    line len 0 >
    line 0 nth "#" != and {
        line echo
    } if
} dolist

# ===== Practical Example: Simple Text Processing =====
"" echo
"=== Simple Text Processing ===" echo

"The quick brown fox jumps over the lazy dog.
The dog was not amused." "sample.txt" write-to-file

"sample.txt" read-from-file text =

"Text length:" echo
text len echo

# ===== Cleanup Note =====
"" echo
"=== Note ===" echo
"The following files were created:" echo
"- test_output.txt" echo
"- multiline.txt" echo
"- data.csv" echo
"- numbers.txt" echo
"- app.log" echo
"- config.txt" echo
"- sample.txt" echo
"You may want to delete them after testing." echo


--- stacker/examples/advanced/string_operations.stk ---
# String Operations - String manipulation techniques

# ===== Basic String Operations =====
"=== Basic String Operations ===" echo

# String concatenation
"Hello" " " + "World!" + echo

# String conversion
42 str echo
3.14 str echo

# ===== String Properties =====
"" echo
"=== String Properties ===" echo

"Length of 'Hello':" echo
"Hello" len echo

"Length of empty string:" echo
"" len echo

# ===== String Access =====
"" echo
"=== String Access ===" echo

# Get character at index (using nth)
"First char:" echo
"Stacker" 0 nth echo

"Char at index 3:" echo
"Stacker" 3 nth echo

# ===== String Comparison =====
"" echo
"=== String Comparison ===" echo

"Is 'apple' < 'banana'?" echo
"apple" "banana" < echo

"Is 'hello' == 'hello'?" echo
"hello" "hello" == echo

"Is 'abc' > 'xyz'?" echo
"abc" "xyz" > echo

# ===== Info =====
"" echo
"=== Note ===" echo
"Basic operations: concatenation (+), length (len), indexing (nth)" echo


--- stacker/examples/advanced/eval_examples.stk ---
# eval - Dynamic code execution

# ===== Basic eval =====
"=== Basic eval ===" echo

# eval executes a code block
{5 3 +} eval echo

{10 2 *} eval echo

# ===== eval vs Direct Execution =====
"" echo
"=== eval vs Direct Execution ===" echo

# Direct execution
"Direct: 5 + 3 =" echo
5 3 + echo

# With eval
"eval: {5 3 +} eval =" echo
{5 3 +} eval echo

# ===== Dynamic Code Construction =====
"" echo
"=== Dynamic Code Construction ===" echo

# Store operation as code block
{2 *} double_op =
"5 * 2 =" echo
5 double_op eval echo

{3 +} add3_op =
"10 + 3 =" echo
10 add3_op eval echo

# ===== eval with Variables =====
"" echo
"=== eval with Variables ===" echo

10 x =
"x + 5 =" echo
{x 5 +} eval echo

# ===== Nested eval =====
"" echo
"=== Nested eval ===" echo

"{{5 3 +}} eval eval =" echo
{{5 3 +}} eval eval echo

# ===== Code as Data =====
"" echo
"=== Code as Data ===" echo

# Store multiple operations
{5 3 +} add_code =
{5 3 -} sub_code =
{5 3 *} mul_code =
{5 3 /} div_code =

"Addition:" echo
add_code eval echo

"Subtraction:" echo
sub_code eval echo

"Multiplication:" echo
mul_code eval echo

"Division:" echo
div_code eval echo

# ===== Conditional eval =====
"" echo
"=== Conditional eval ===" echo

true condition =

condition {
    "Condition true, 10+20 =" echo
    {10 20 +} eval echo
} {
    "Condition false, 10*20 =" echo
    {10 20 *} eval echo
} ifelse

# ===== Macro-like Behavior =====
"" echo
"=== Macro-like Behavior with eval ===" echo

# Create a "macro" that repeats an operation
{code times} {
    0 times i {
        code eval
    } do
} repeat_eval defun

"Repeating 'Hello' 3 times:" echo
{"Hello" echo} 3 repeat_eval

# ===== Practical Example: Apply Operation =====
"" echo
"=== Apply Operation Example ===" echo

{operation a b} {
    a b operation eval
} apply defun

"5 + 3 =" echo
{+} 5 3 apply echo

"5 * 3 =" echo
{*} 5 3 apply echo

# ===== Security Note =====
"" echo
"=== Security Warning ===" echo
"eval executes arbitrary code!" echo
"Only use with trusted input." echo
"Never eval user input directly in production." echo

# ===== Performance Note =====
"" echo
"=== Performance Note ===" echo
"eval has overhead - use direct execution when possible" echo


--- stacker/test/test_inline_comments.py ---
import unittest
from pathlib import Path
import tempfile
import os

from stacker.stacker import Stacker
from stacker.runtime.exec_modes.script_mode import ScriptMode


class TestInlineComments(unittest.TestCase):
    def setUp(self):
        self.stacker = Stacker()
        self.script_mode = ScriptMode(self.stacker)

    def test_simple_inline_comment(self):
        """Test that inline comments are ignored"""
        self.stacker.stack.clear()
        ans = self.stacker.eval("3 4 +  # This is a comment")
        self.assertEqual(ans[-1], 7)

    def test_inline_comment_in_script(self):
        """Test inline comments in script files"""
        script_content = """
0 counter set  # Initialize counter
counter 1 + counter set  # Increment
counter  # Push to stack
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            self.assertEqual(self.stacker.stack[-1], 1)
        finally:
            os.unlink(temp_file)

    def test_multiline_function_with_inline_comments(self):
        """Test function definition across multiple lines with inline comments"""
        script_content = """
{x y}  # Parameters
{x y *}  # Function body
multiply defun  # Define function

10 20 multiply  # Call function
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            self.assertEqual(self.stacker.stack[-1], 200)
        finally:
            os.unlink(temp_file)

    def test_inline_comment_inside_block(self):
        """Test inline comments inside code blocks"""
        script_content = """
{x} {
    x 2 *  # Double the value
} double defun

5 double
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            self.assertEqual(self.stacker.stack[-1], 10)
        finally:
            os.unlink(temp_file)

    def test_inline_comment_with_special_chars(self):
        """Test inline comments with special characters"""
        script_content = """
3 4 +  # Comment with special chars: {}[]()'"
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            self.assertEqual(self.stacker.stack[-1], 7)
        finally:
            os.unlink(temp_file)

    def test_hash_in_string_not_comment(self):
        """Test that # inside strings is not treated as comment"""
        self.stacker.stack.clear()
        ans = self.stacker.eval('"Hello # World"')
        self.assertEqual(ans[-1], "Hello # World")

    def test_hash_in_string_with_comment(self):
        """Test string with # and actual comment"""
        self.stacker.stack.clear()
        ans = self.stacker.eval('"Hash: #" # This is a comment')
        self.assertEqual(ans[-1], "Hash: #")

    def test_multiline_with_comment_after_brace(self):
        """Test comment after opening brace"""
        script_content = """
{x y}  # Parameters
{  # Start of body
    x y +  # Add them
}  # End of body
add defun

3 4 add
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            self.assertEqual(self.stacker.stack[-1], 7)
        finally:
            os.unlink(temp_file)

    def test_comment_with_code_after_on_same_line(self):
        """Test that code after comment on same line is ignored"""
        script_content = """
3 4  # This is ignored + 10 20
+
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # Should be 7 (3+4), not 17 (3+4+10) or other
            self.assertEqual(self.stacker.stack[-1], 7)
        finally:
            os.unlink(temp_file)

    def test_line_comment_at_start(self):
        """Test that lines starting with # are skipped"""
        script_content = """
# This is a full line comment
3 4 +
# Another comment
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            self.assertEqual(self.stacker.stack[-1], 7)
        finally:
            os.unlink(temp_file)

    def test_empty_line_after_inline_comment(self):
        """Test that inline comment doesn't affect subsequent lines"""
        script_content = """
3  # First number

4  # Second number
+  # Add them
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            self.assertEqual(self.stacker.stack[-1], 7)
        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    unittest.main()


--- stacker/test/test_no_dollar_in_blocks.py ---
"""Tests for using operator names as variables without $ prefix."""

import unittest
from stacker import Stacker


class TestOperatorNamesAsVariables(unittest.TestCase):
    """Test that operator names can be used as variable names without $."""

    def test_sum_as_variable(self):
        """Test using 'sum' (a built-in operator) as a variable name."""
        stacker = Stacker()
        result = stacker.eval("10 sum set sum")
        self.assertEqual(result[-1], 10)

    def test_sum_in_block_reassignment(self):
        """Test reassigning 'sum' variable inside a block."""
        stacker = Stacker()
        result = stacker.eval("0 sum set 1 3 i {sum i + sum set} do sum")
        self.assertEqual(result[-1], 6)  # 0 + 1 + 2 + 3 = 6

    def test_max_as_variable(self):
        """Test using 'max' (a built-in operator) as a variable name."""
        stacker = Stacker()
        result = stacker.eval("42 max set max")
        self.assertEqual(result[-1], 42)

    def test_min_as_variable(self):
        """Test using 'min' (a built-in operator) as a variable name."""
        stacker = Stacker()
        result = stacker.eval("99 min set min")
        self.assertEqual(result[-1], 99)

    def test_operator_name_in_dolist(self):
        """Test using operator name as accumulator in dolist."""
        stacker = Stacker()
        result = stacker.eval(
            "1 product set [2 3 4] x {product x * product set} dolist product"
        )
        self.assertEqual(result[-1], 24)  # 1 * 2 * 3 * 4 = 24

    def test_mixed_operator_and_variable(self):
        """Test that operators still work when not followed by 'set'."""
        stacker = Stacker()
        result = stacker.eval("[1 2 3 4 5] sum")
        # 'sum' should be called as operator, not variable
        self.assertEqual(result[-1], 15)

    def test_variable_then_operator_same_name(self):
        """Test using a name as both variable and operator."""
        stacker = Stacker()
        stacker.eval("100 sum set")  # Set sum as variable
        result = stacker.eval("sum")  # Get variable value
        self.assertEqual(result[-1], 100)

        # Now use sum as operator
        stacker2 = Stacker()
        result2 = stacker2.eval("[1 2 3] sum")
        self.assertEqual(result2[-1], 6)


if __name__ == "__main__":
    unittest.main()


--- stacker/test/test_defmacro.py ---
import unittest

from stacker.stacker import Stacker


class TestStacker(unittest.TestCase):
    def setUp(self):
        self.stacker = Stacker()

    def test_macro_definition_and_call_1(self):
        self.stacker.stack.clear()
        self.stacker.eval("{4 +} $add defmacro")
        ans = self.stacker.eval("3 add")
        self.assertEqual(ans[-1], 7)


--- stacker/test/test_string_apostrophe.py ---
"""Test for string literals containing apostrophes.

This tests the fix for the bug where apostrophes inside string literals
would break tokenization.
"""

import pytest
from stacker.stacker import Stacker


def test_apostrophe_in_string():
    """Test that apostrophes in double-quoted strings work correctly."""
    stacker = Stacker()
    # Just verify it doesn't cause a syntax error
    stacker.eval('"won\'t" drop')
    assert len(stacker.stack) == 0  # drop removed it from stack


def test_apostrophe_in_code_block_with_if():
    """Test apostrophe in string inside code block with if statement."""
    stacker = Stacker()
    stacker.eval('true {"This won\'t fail" echo} if')
    # echo doesn't push to stack, but we can verify no error occurred
    assert True  # If we got here, it worked


def test_apostrophe_with_false_condition():
    """Test apostrophe in string with false condition (shouldn't execute)."""
    stacker = Stacker()
    stacker.eval('false {"This won\'t print" echo} if')
    # Stack should be empty since the block didn't execute
    assert len(stacker.stack) == 0


def test_multiple_apostrophes():
    """Test multiple apostrophes in a string."""
    stacker = Stacker()
    stacker.eval('"It\'s working! Don\'t worry." drop')
    assert len(stacker.stack) == 0  # drop removed it from stack


def test_apostrophe_in_nested_blocks():
    """Test apostrophe in nested code blocks."""
    stacker = Stacker()
    stacker.eval('true {true {"won\'t"} if} if')
    result = stacker.stack.pop()
    assert result == "won't"


def test_apostrophe_with_ifelse():
    """Test apostrophe in ifelse blocks."""
    stacker = Stacker()
    stacker.eval('true {"it\'s true"} {"it\'s false"} ifelse')
    assert stacker.stack.pop() == "it's true"

    stacker = Stacker()
    stacker.eval('false {"it\'s true"} {"it\'s false"} ifelse')
    assert stacker.stack.pop() == "it's false"


def test_escaped_quotes():
    """Test escaped quotes in strings."""
    stacker = Stacker()
    stacker.eval('"Testing \\"quotes\\" inside" drop')
    assert len(stacker.stack) == 0  # Verifies no syntax error


def test_escaped_quotes_with_apostrophe():
    """Test both escaped quotes and apostrophes together."""
    stacker = Stacker()
    stacker.eval('"It\\"s a \\"test\\" that won\'t fail" drop')
    assert len(stacker.stack) == 0  # Verifies no syntax error


--- stacker/test/test_lambda.py ---
import unittest

from stacker.stacker import Stacker


class TestStacker(unittest.TestCase):
    def setUp(self):
        self.stacker = Stacker()

    def test_test_lambda_1(self):
        self.stacker.stack.clear()
        ans = self.stacker.eval("[1 2 3] {x} {x 2 *} lambda map")
        self.assertEqual(ans[-1], [2, 4, 6])

    # REMOVED: test_test_lambda_2 - () now creates code blocks, not tuples
    # Use [1 2 3] for lists instead

    def test_test_lambda_3(self):
        self.stacker.stack.clear()
        ans = self.stacker.eval("{1 2 3} {x} {x 2 *} lambda map")
        self.assertEqual(list(ans[-1]), [2, 4, 6])

    def test_test_lambda_factorial(self):
        self.stacker.stack.clear()
        ans = self.stacker.eval(
            """
{ n } {
    n 1 <=
    { 1 }
    { n n 1 - fact * }
    ifelse
} lambda $fact set
5 fact eval
"""
        )
        self.assertEqual(ans[-1], 120)


--- stacker/test/test_no_dollar_syntax.py ---
"""Tests for the new syntax without $ prefix for variable names."""

import unittest
from stacker import Stacker


class TestNoDollarSyntax(unittest.TestCase):
    """Test cases for variable/function definitions without $ prefix."""

    def setUp(self):
        """Set up a fresh Stacker instance for each test."""
        self.stacker = Stacker()

    def test_set_without_dollar(self):
        """Test variable assignment without $ prefix."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval("3 x set x")
        self.assertEqual(result[-1], 3)

    def test_set_multiple_variables_without_dollar(self):
        """Test multiple variable assignments without $ prefix."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval("5 x set 10 y set x y +")
        self.assertEqual(result[-1], 15)

    def test_set_with_dollar_backward_compatibility(self):
        """Test that $ prefix still works (backward compatibility)."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval("100 $legacy set legacy")
        self.assertEqual(result[-1], 100)

    def test_set_mixed_syntax(self):
        """Test mixing $ and non-$ syntax."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval("10 $x set 20 y set x y +")
        self.assertEqual(result[-1], 30)

    def test_defun_without_dollar(self):
        """Test function definition without $ prefix."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval("{a b} {a b +} add defun 5 10 add")
        self.assertEqual(result[-1], 15)

    def test_defun_with_dollar_backward_compatibility(self):
        """Test that defun with $ prefix still works."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval("{a b} {a b *} $multiply defun 3 4 multiply")
        self.assertEqual(result[-1], 12)

    def test_defmacro_without_dollar(self):
        """Test macro definition without $ prefix."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval("{2 *} double defmacro 5 double")
        self.assertEqual(result[-1], 10)

    def test_defmacro_with_dollar_backward_compatibility(self):
        """Test that defmacro with $ prefix still works."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval("{3 +} $addThree defmacro 10 addThree")
        self.assertEqual(result[-1], 13)

    def test_do_loop_without_dollar(self):
        """Test do loop without $ prefix (variable name in do)."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval("0 sum set 1 5 i {sum i + sum set} do sum")
        # Sum of 1 to 5 = 15
        self.assertEqual(result[-1], 15)

    def test_do_loop_with_dollar_backward_compatibility(self):
        """Test that do loop with $ prefix still works."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval("0 $total set 1 3 $i {total i + total set} do total")
        # Sum of 1 to 3 = 6
        self.assertEqual(result[-1], 6)

    def test_dolist_without_dollar(self):
        """Test dolist without $ prefix (variable name in dolist)."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval("0 sum set [10 20 30] x {sum x + sum set} dolist sum")
        # Sum of 10, 20, 30 = 60
        self.assertEqual(result[-1], 60)

    def test_dolist_with_dollar_backward_compatibility(self):
        """Test that dolist with $ prefix still works."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval(
            "0 $total set [5 15 25] $x {total x + total set} dolist total"
        )
        # Sum of 5, 15, 25 = 45
        self.assertEqual(result[-1], 45)

    def test_undefined_variable_becomes_undefined_symbol(self):
        """Test that undefined variables are treated as UndefinedSymbol objects (not errors)."""
        from stacker.engine.data_type import UndefinedSymbol

        stacker = Stacker()  # Fresh instance
        result = stacker.eval("undefined_var")
        # Undefined variable should be pushed as an UndefinedSymbol
        self.assertIsInstance(result[-1], UndefinedSymbol)
        self.assertEqual(str(result[-1]), "undefined_var")

    def test_undefined_symbol_raises_error_when_used(self):
        """Test that UndefinedSymbol raises error when used in operations."""
        stacker = Stacker()  # Fresh instance
        # Using an undefined variable in arithmetic should raise an error
        with self.assertRaises(Exception):
            stacker.eval("5 undefined_var +")

    def test_string_variable_name_still_works(self):
        """Test that string-based variable names still work."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval('5 "stringvar" set stringvar')
        self.assertEqual(result[-1], 5)

    def test_equal_operator_without_dollar(self):
        """Test = operator without $ prefix."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval("42 x = x")
        self.assertEqual(result[-1], 42)

    def test_equal_operator_multiple_variables(self):
        """Test multiple variable assignments with = operator without $ prefix."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval("7 a = 8 b = a b *")
        self.assertEqual(result[-1], 56)

    def test_equal_operator_with_dollar_backward_compatibility(self):
        """Test that = operator with $ prefix still works."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval("99 $value = value")
        self.assertEqual(result[-1], 99)

    def test_equal_operator_mixed_syntax(self):
        """Test mixing $ and non-$ syntax with = operator."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval("15 $x = 25 y = x y +")
        self.assertEqual(result[-1], 40)

    def test_equal_vs_set_equivalence(self):
        """Test that = and set operators are equivalent."""
        stacker1 = Stacker()  # Fresh instance
        stacker2 = Stacker()  # Fresh instance
        result1 = stacker1.eval("10 x set 20 y set x y *")
        result2 = stacker2.eval("10 x = 20 y = x y *")
        self.assertEqual(result1[-1], result2[-1])
        self.assertEqual(result1[-1], 200)

    def test_equal_operator_in_function(self):
        """Test = operator inside function without $ prefix."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval("{n} {0 a = 1 b = 2 n i {a b + temp = b a = temp b =} do b} fib defun 10 fib")
        # Fibonacci(10) = 55
        self.assertEqual(result[-1], 55)

    def test_equal_operator_in_loop(self):
        """Test = operator in do loop without $ prefix."""
        stacker = Stacker()  # Fresh instance
        result = stacker.eval("0 total = 1 5 i {total i + total =} do total")
        # Sum of 1 to 5 = 15
        self.assertEqual(result[-1], 15)


if __name__ == "__main__":
    unittest.main()


--- stacker/test/__init__.py ---


--- stacker/test/test_reduce.py ---
"""Tests for reduce and fold higher-order functions."""

import unittest
from stacker.stacker import Stacker


class TestReduce(unittest.TestCase):
    """Test reduce/fold functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.stacker = Stacker()

    def test_reduce_sum(self):
        """Test reduce to sum a list."""
        # [1 2 3 4 5] 0 acc x {acc x +} reduce
        self.stacker.process_expression("[1 2 3 4 5] 0 acc x {acc x +} reduce")
        result = self.stacker.pop()
        self.assertEqual(result, 15)

    def test_reduce_product(self):
        """Test reduce to multiply all elements."""
        # [1 2 3 4 5] 1 acc x {acc x *} reduce
        self.stacker.process_expression("[1 2 3 4 5] 1 acc x {acc x *} reduce")
        result = self.stacker.pop()
        self.assertEqual(result, 120)

    def test_fold_sum(self):
        """Test fold (alias for reduce) to sum a list."""
        self.stacker.process_expression("[1 2 3 4 5] 0 acc x {acc x +} fold")
        result = self.stacker.pop()
        self.assertEqual(result, 15)

    def test_reduce_with_strings(self):
        """Test reduce with string concatenation."""
        self.stacker.process_expression('["a" "b" "c"] "" acc x {acc x concat} reduce')
        result = self.stacker.pop()
        self.assertEqual(result, "abc")

    def test_reduce_empty_list(self):
        """Test reduce with empty list returns initial value."""
        self.stacker.process_expression("[] 42 acc x {acc x +} reduce")
        result = self.stacker.pop()
        self.assertEqual(result, 42)

    def test_reduce_single_element(self):
        """Test reduce with single element."""
        self.stacker.process_expression("[5] 0 acc x {acc x +} reduce")
        result = self.stacker.pop()
        self.assertEqual(result, 5)

    def test_reduce_max(self):
        """Test reduce to find maximum."""
        # [3 7 2 9 1] -999999 acc x {acc x < {x} {acc} ifelse} reduce
        self.stacker.process_expression("[3 7 2 9 1] -999999 acc x {acc x < {x} {acc} ifelse} reduce")
        result = self.stacker.pop()
        self.assertEqual(result, 9)

    def test_reduce_count(self):
        """Test reduce to count elements."""
        # [1 2 3 4 5] 0 acc x {acc 1 +} reduce
        self.stacker.process_expression("[1 2 3 4 5] 0 acc x {acc 1 +} reduce")
        result = self.stacker.pop()
        self.assertEqual(result, 5)

    def test_reduce_with_nested_operations(self):
        """Test reduce with complex nested operations."""
        # Square each element and sum: [1 2 3 4] 0 acc x {acc x x * +} reduce
        self.stacker.process_expression("[1 2 3 4] 0 acc x {acc x x * +} reduce")
        result = self.stacker.pop()
        self.assertEqual(result, 30)  # 1^2 + 2^2 + 3^2 + 4^2 = 1 + 4 + 9 + 16 = 30


if __name__ == "__main__":
    unittest.main()


--- stacker/test/test_include.py ---
import unittest

from stacker.stacker import Stacker
from pathlib import Path
from stacker.error import IncludeError
from stacker.include.include import include_stacker_script


# class TestImportStacker(unittest.TestCase):
#     def test_include(self):
#         filename = "test/src_test/test.stk"
#         stacker = Stacker()
#         stacker.stack.clear()
#         stacker.process_expression(f"'{filename}' include")
#         stacker.process_expression("5 increment")
#         self.assertEqual(stacker.stack[-1], 6)
class TestImportStacker(unittest.TestCase):
    def test_include(self):
        filename = "test/src_test/test.stk"
        stacker = Stacker()
        stacker.stack.clear()
        stacker.process_expression(f"'{filename}' include")
        stacker.process_expression("5 increment")
        self.assertEqual(stacker.stack[-1], 6)

    def test_include_stacker_script_valid(self):
        filename = "test/src_test/test.stk"
        stacker = include_stacker_script(filename)
        self.assertIsInstance(stacker, Stacker)

    def test_include_stacker_script_invalid_extension(self):
        filename = "test/src_test/test.txt"
        with self.assertRaises(IncludeError) as context:
            include_stacker_script(filename)
        self.assertIn("File test/src_test/test.txt not found.", str(context.exception))

    def test_include_stacker_script_file_not_found(self):
        filename = "test/src_test/non_existent.stk"
        with self.assertRaises(IncludeError) as context:
            include_stacker_script(filename)
        self.assertIn(
            "File test/src_test/non_existent.stk not found", str(context.exception)
        )

    def test_include_stacker_script_invalid_path(self):
        filename = Path("test/src_test/test.stk")
        stacker = include_stacker_script(filename)
        self.assertIsInstance(stacker, Stacker)


if __name__ == "__main__":
    unittest.main()


--- stacker/test/test_stacker.py ---
import cmath
import math
import unittest

from stacker.stacker import Stacker

from stacker.syntax.lexer import lex_string
from stacker.engine.data_type import String


def cpow(x1, x2):
    return cmath.exp(x2 * cmath.log(x1))


class TestUnit(unittest.TestCase):
    def setUp(self):
        self.stacker = Stacker()

    def test_lex_string(self):
        expr = "1 2 3 [4 5 6] 7 8 (9 10 11) a1 b1 c1 {1 2 +} '1+1' eval"
        exprs = [
            "1",
            "2",
            "3",
            "[4 5 6]",
            "7",
            "8",
            "(9 10 11)",
            "a1",
            "b1",
            "c1",
            "{1 2 +}",
            "'1+1'",
            "eval",
        ]
        result = lex_string(expr)
        self.assertEqual(result, exprs)

    def test_lex_string_2(self):
        expr = "'1+1' eval"
        exprs = ["'1+1'", "eval"]
        result = lex_string(expr)
        print(result)
        self.assertEqual(result, exprs)


class TestStacker(unittest.TestCase):
    def setUp(self):
        self.stacker = Stacker()

    def test_operations(self):
        test_cases = [
            ("2 3 +", 5),
            ("10 3 -", 7),
            ("4 6 *", 24),
            ("12 4 /", 3),
            ("7 2 //", 3),
            ("9 2 %", 1),
            ("5 neg", -5),
            ("3 neg abs", 3),
            ("3 2 ^", 9),
            ("3 exp", math.exp(3)),
            ("2 log", math.log(2)),
            ("30 radians sin", math.sin(math.radians(30))),
            ("45 radians cos", math.cos(math.radians(45))),
            ("60 radians tan", math.tan(math.radians(60))),
            ("5 float", 5.0),
            ("3.14 int", 3),
            ("1 1 ==", True),
            ("1 0 !=", True),
            ("1 2 <", True),
            ("3 3 <=", True),
            ("2 1 >", True),
            ("3 3 >=", True),
            ("true false and", False),
            ("true false or", True),
            ("true not", False),
            ("3 2 band", 3 & 2),
            ("3 2 bor", 3 | 2),
            ("3 2 bxor", 3 ^ 2),
            ("8 2 >>", 2),
            ("2 2 <<", 8),
            ("5 ~", -6),
            ("5 bin", "0b101"),
            ("10 oct", "0o12"),
            ("0b101010 dec", 42),
            ("255 hex", "0xff"),
            ("4 2 gcd", math.gcd(4, 2)),
            ("4 log10", math.log10(4)),
            ("4 log2", math.log2(4)),
            ("4 !", math.factorial(4)),
            ("9 sqrt", math.sqrt(9)),
            ("3.2 ceil", math.ceil(3.2)),
            ("3.8 floor", math.floor(3.8)),
            ("3.5 round", round(3.5)),
            ("3.51 1 roundn", round(3.51, 1)),
            # Add complex number test cases
            ("(1+2j) (2+3j) +", complex(1, 2) + complex(2, 3)),
            ("(1+2j) (2+3j) -", complex(1, 2) - complex(2, 3)),
            ("(1+2j) (2+3j) *", complex(1, 2) * complex(2, 3)),
            ("(1+2j) (2+3j) /", complex(1, 2) / complex(2, 3)),
            ("(1+2j) 2 ^", complex(1, 2) ** 2),
            ("(1+2j) exp", cmath.exp(complex(1, 2))),
            ("(1+2j) log", cmath.log(complex(1, 2))),
            ("(1+2j) sin", cmath.sin(complex(1, 2))),
            ("(1+2j) cos", cmath.cos(complex(1, 2))),
            ("(1+2j) tan", cmath.tan(complex(1, 2))),
            ("(1+2j) sqrt", cmath.sqrt(complex(1, 2))),
            ("(1+2j) sinh", cmath.sinh(complex(1, 2))),
            ("(1+2j) cosh", cmath.cosh(complex(1, 2))),
            ("(1+2j) tanh", cmath.tanh(complex(1, 2))),
            ("(1+2j) asin", cmath.asin(complex(1, 2))),
            ("(1+2j) acos", cmath.acos(complex(1, 2))),
            ("(1+2j) atan", cmath.atan(complex(1, 2))),
            ("(1+2j) asinh", cmath.asinh(complex(1, 2))),
            ("(1+2j) acosh", cmath.acosh(complex(1, 2))),
            ("(1+2j) atanh", cmath.atanh(complex(1, 2))),
            ("4 2 lcm", math.lcm(4, 2)),
            ("27 cbrt", 27 ** (1 / 3)),
            ("5 2 ncr", math.comb(5, 2)),
            ("5 2 npr", math.perm(5, 2)),
        ]

        for expression, expected in test_cases:
            self.stacker.stack.clear()
            try:
                self.stacker.process_expression(expression)
            except Exception:
                print("error!!", expression)
                assert False
            try:
                self.assertEqual(self.stacker.stack[-1], expected)
            except Exception:
                print("error!!", expression)
                assert False
        for expression, expected in test_cases:
            self.stacker.stack.clear()
            self.stacker.process_expression(expression)
            self.assertAlmostEqual(self.stacker.stack[-1], expected)

    def test_long_rpn(self):
        self.stacker.stack.clear()
        expression = " 8 3 5 * 2 / + 7 4 + neg 2 ^ 1 3 + * -"
        self.stacker.process_expression(expression)
        self.assertEqual(self.stacker.stack[-1], -468.5)

    def test_stack_operations(self):
        # Test 'copy' operation
        # self.stacker.stack.clear()
        # self.stacker.process_expression("1 2 3 4 5")
        # self.stacker.process_expression("1 copy")
        # self.assertEqual(self.stacker.stack, [1, 2, 3, 4, 5, 2])

        # Test 'pop' operation
        self.stacker.stack.clear()
        self.stacker.process_expression("1 2 3 4 5")
        self.stacker.process_expression("drop")
        self.assertEqual(list(self.stacker.stack), [1, 2, 3, 4])

        # Test 'dup' operation
        self.stacker.stack.clear()
        self.stacker.process_expression("1 2 3 4 5")
        self.stacker.process_expression("dup")
        self.assertEqual(list(self.stacker.stack), [1, 2, 3, 4, 5, 5])

        # Test 'rev' operation
        self.stacker.stack.clear()
        self.stacker.process_expression("1 2 3 4 5")
        self.assertEqual(list(self.stacker.stack), [1, 2, 3, 4, 5])
        self.stacker.process_expression("rev")
        self.assertEqual(list(self.stacker.stack), [5, 4, 3, 2, 1])

    def test_variable_assignment(self):
        self.stacker.stack.clear()
        self.stacker.process_expression("5 $a set")
        self.assertEqual(self.stacker.variables["a"], 5)

    def test_function_definition_and_call(self):
        self.stacker.stack.clear()
        self.stacker.process_expression("{x} {x x *} $f defun")
        self.stacker.process_expression("4 f")
        self.assertEqual(self.stacker.stack[-1], 16)

    def test_input(self):
        # int
        self.stacker.process_expression("5")
        self.assertEqual(self.stacker.stack[-1], 5)
        self.assertEqual(type(self.stacker.stack[-1]), int)

        # float
        self.stacker.process_expression("5.0")
        self.assertEqual(self.stacker.stack[-1], 5.0)
        self.assertEqual(type(self.stacker.stack[-1]), float)

        self.stacker.process_expression("3.")
        self.assertEqual(self.stacker.stack[-1], 3.0)
        self.assertEqual(type(self.stacker.stack[-1]), float)

        # str
        self.stacker.process_expression("'hoge'")
        self.assertEqual(self.stacker.stack[-1], "hoge")
        self.assertEqual(type(self.stacker.stack[-1]), String)

        # REMOVED: tuple test - () now creates code blocks, not tuples

        # list
        self.stacker.process_expression("[1 2 3]")
        self.assertEqual(self.stacker.stack[-1], [1, 2, 3])
        self.assertEqual(type(self.stacker.stack[-1]), list)

        # complex
        self.stacker.process_expression("4j")
        self.assertEqual(self.stacker.stack[-1], complex(4j))
        self.assertEqual(type(self.stacker.stack[-1]), complex)

        ...

    def test_list_input(self):
        # # Standard list input
        # self.stacker.process_expression("[1, 2, 3]")
        # self.assertEqual(self.stacker.stack[-1], [1, 2, 3])

        # self.stacker.process_expression(
        #     "[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]"
        # )
        # self.assertEqual(self.stacker.stack[-1], [10, 11, 12])
        # self.assertEqual(self.stacker.stack[-2], [7, 8, 9])
        # self.assertEqual(self.stacker.stack[-3], [4, 5, 6])
        # self.assertEqual(self.stacker.stack[-4], [1, 2, 3])

        # self.stacker.process_expression(
        #     "[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]"
        # )
        # self.assertEqual(self.stacker.stack[-1], [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])

        self.stacker.process_expression("[1 2 3]")
        self.assertEqual(self.stacker.stack[-1], [1, 2, 3])

        self.stacker.process_expression("[1 2 3] 4")
        self.assertEqual(self.stacker.stack[-1], 4)
        self.assertEqual(self.stacker.stack[-2], [1, 2, 3])

        # Custom format list input with float
        self.stacker.process_expression("[1.0 2.0 3.0]")
        self.assertEqual(self.stacker.stack[-1], [1.0, 2.0, 3.0])

        # Multiline input
        self.stacker.process_expression("[1 2 3 ; 4 5 6]")
        self.assertEqual(self.stacker.stack[-1], [[1, 2, 3], [4, 5, 6]])

        self.stacker.process_expression("[1 2 3; 4 5 6; 7 8 9]")
        self.assertEqual(self.stacker.stack[-1], [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        self.stacker.process_expression("[1 2 3; 4 5 6; 7 8 9] 5 6")
        self.assertEqual(self.stacker.stack[-1], 6)
        self.assertEqual(self.stacker.stack[-2], 5)
        self.assertEqual(self.stacker.stack[-3], [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    # REMOVED: test_tuple_input - () now creates code blocks, not tuples
    # All tuple-related assertions removed

    # REMOVED: Tuple multiline input tests
    # Tuples no longer exist - () now creates code blocks identical to {}
    # Use lists [] for data structures instead

    # valiable
    def test_variable_assign_1(self):
        self.stacker.stack.clear()
        self.stacker.process_expression("123 $a set")
        self.stacker.process_expression("a")
        self.assertEqual(self.stacker.pop_and_eval(self.stacker.stack), 123)

    def test_variable_assign_2(self):
        self.stacker.stack.clear()
        self.stacker.process_expression("{30 50 +} $b set")
        self.stacker.process_expression("b")
        # self.stacker.process_expression("pop")
        self.assertEqual(self.stacker.pop_and_eval(self.stacker.stack), 80)

    # blockstack
    def test_blockstack(self):
        self.stacker.stack.clear()
        self.stacker.process_expression("1 {3 {4 5 +} *} +")
        self.assertEqual(self.stacker.stack[-1], 28)

    # eval
    def test_eval_str(self):
        self.stacker.stack.clear()
        self.stacker.process_expression("'3 5 +' eval")
        self.assertEqual(self.stacker.stack[-1], 8)

        self.stacker.stack.clear()
        self.stacker.process_expression("5 eval")
        self.assertEqual(self.stacker.stack[-1], 5)

    def test_eval_block(self):
        self.stacker.stack.clear()
        self.stacker.process_expression("{3 5 +} eval")
        self.assertEqual(self.stacker.stack[-1], 8)

        self.stacker.stack.clear()
        self.stacker.process_expression("{3 5} {*} eval")
        self.assertEqual(self.stacker.stack[-1], 15)

    def test_eval_list(self):
        self.stacker.stack.clear()
        self.stacker.process_expression("'[3 5 6]' eval")
        self.assertEqual(self.stacker.stack[-1], [3, 5, 6])

    # REMOVED: test_eval_tuple - () now creates code blocks, not tuples

    def test_eval_variable(self):
        self.stacker.stack.clear()
        self.stacker.process_expression("5 $a set")
        self.stacker.process_expression("a eval")
        self.assertEqual(self.stacker.stack[-1], 5)


if __name__ == "__main__":
    unittest.main()


--- stacker/test/test_aggregate.py ---
import unittest

from stacker.stacker import Stacker


class TestUnit(unittest.TestCase):
    ############################
    # any
    ############################
    def test_any_block_true_1(self):
        stacker = Stacker()
        ans = stacker.eval("{true true true} any")
        self.assertEqual(ans[-1], True)

    def test_any_block_true_2(self):
        stacker = Stacker()
        ans = stacker.eval("{true false true} any")
        self.assertEqual(ans[-1], True)

    def test_any_list_true_1(self):
        stacker = Stacker()
        ans = stacker.eval("[true true true] any")
        self.assertEqual(ans[-1], True)

    def test_any_list_true_2(self):
        stacker = Stacker()
        ans = stacker.eval("[true false true] any")
        self.assertEqual(ans[-1], True)

    def test_any_list_false(self):
        stacker = Stacker()
        ans = stacker.eval("[false false false] any")
        self.assertEqual(ans[-1], False)

    # REMOVED: test_any_tuple_* - () now creates code blocks, not tuples

    ############################
    # all
    ############################
    def test_all_block_true(self):
        stacker = Stacker()
        ans = stacker.eval("{true true true} all")
        self.assertEqual(ans[-1], True)

    def test_all_block_false(self):
        stacker = Stacker()
        ans = stacker.eval("{true false true} all")
        self.assertEqual(ans[-1], False)

    def test_all_list_true(self):
        stacker = Stacker()
        ans = stacker.eval("[true true true] all")
        self.assertEqual(ans[-1], True)

    def test_all_list_false(self):
        stacker = Stacker()
        ans = stacker.eval("[true false true] all")
        self.assertEqual(ans[-1], False)

    # REMOVED: test_all_tuple_* - () now creates code blocks, not tuples

    ############################
    # sum
    ############################
    def test_sum_block(self):
        stacker = Stacker()
        ans = stacker.eval("{1 2 3} sum")
        self.assertEqual(ans[-1], 6)

    def test_sum_list(self):
        stacker = Stacker()
        ans = stacker.eval("[1 2 3] sum")
        self.assertEqual(ans[-1], 6)

    # REMOVED: test_sum_tuple - () now creates code blocks, not tuples

    ############################
    # max
    ############################
    def test_max_block(self):
        stacker = Stacker()
        ans = stacker.eval("{1 2 3} max")
        self.assertEqual(ans[-1], 3)

    def test_max_list(self):
        stacker = Stacker()
        ans = stacker.eval("[1 2 3] max")
        self.assertEqual(ans[-1], 3)

    # REMOVED: test_max_tuple - () now creates code blocks, not tuples

    ############################
    # min
    ############################
    def test_min_block(self):
        stacker = Stacker()
        ans = stacker.eval("{1 2 3} min")
        self.assertEqual(ans[-1], 1)

    def test_min_list(self):
        stacker = Stacker()
        ans = stacker.eval("[1 2 3] min")
        self.assertEqual(ans[-1], 1)

    # REMOVED: test_min_tuple - () now creates code blocks, not tuples

    ############################
    # len
    ############################
    def test_len_block(self):
        stacker = Stacker()
        ans = stacker.eval("{1 2 3} len")
        self.assertEqual(ans[-1], 3)

    def test_len_list(self):
        stacker = Stacker()
        ans = stacker.eval("[1 2 3] len")
        self.assertEqual(ans[-1], 3)

    # REMOVED: test_len_tuple - () now creates code blocks, not tuples


--- stacker/test/test_scope.py ---
import unittest
from pathlib import Path
import tempfile
import os

from stacker.stacker import Stacker
from stacker.runtime.exec_modes.script_mode import ScriptMode


class TestVariableScope(unittest.TestCase):
    """Test variable scoping behavior."""

    def setUp(self):
        self.stacker = Stacker()

    def test_global_variable_access_from_function(self):
        """Test that functions can $access global variables."""
        self.stacker.stack.clear()
        self.stacker.eval("10 $global_var set")
        self.stacker.eval("{x} {x global_var +} $add_global defun")
        result = self.stacker.eval("5 add_global")
        self.assertEqual(result[-1], 15)

    def test_local_variable_shadows_global(self):
        """Test that local variables $shadow global variables."""
        self.stacker.stack.clear()
        self.stacker.eval("100 $x set")
        self.stacker.eval("{x} {x 2 *} $double defun")
        result = self.stacker.eval("5 double")
        self.assertEqual(result[-1], 10)
        # Global x should still be 100
        result = self.stacker.eval("x")
        self.assertEqual(result[-1], 100)

    def test_function_does_not_modify_global_scope(self):
        """Test that function-local variables don't $affect global scope."""
        self.stacker.stack.clear()
        self.stacker.eval("42 $answer set")
        self.stacker.eval("{n} {n $temp set temp 2 *} $calc defun")
        result = self.stacker.eval("10 calc")
        self.assertEqual(result[-1], 20)
        # Global answer should still be 42
        result = self.stacker.eval("answer")
        self.assertEqual(result[-1], 42)
        # temp should not exist $in global scope - it becomes UndefinedSymbol
        from stacker.engine.data_type import UndefinedSymbol

        result = self.stacker.eval("temp")
        self.assertIsInstance(result[-1], UndefinedSymbol)
        # But using it in an operation should raise an error
        with self.assertRaises(Exception):
            self.stacker.eval("temp 5 +")

    def test_nested_function_calls_independent_scopes(self):
        """Test that nested function calls have independent scopes."""
        self.stacker.stack.clear()
        self.stacker.eval("{x} {x 1 +} $inc defun")
        self.stacker.eval("{x} {x inc inc inc} $inc3 defun")
        result = self.stacker.eval("5 inc3")
        self.assertEqual(result[-1], 8)

    def test_recursive_function_independent_scopes(self):
        """Test that recursive calls maintain independent scopes."""
        self.stacker.stack.clear()
        # Fibonacci: fib(n) = fib(n-1) + fib(n-2), base cases: fib(0)=0, fib(1)=1
        self.stacker.eval("""
            {n} {
                n 2 <
                {n}
                {n 1 - fib n 2 - fib +}
                ifelse
            } $fib defun
        """)
        result = self.stacker.eval("6 fib")
        self.assertEqual(result[-1], 8)  # fib(6) = 8

    def test_multiple_parameters_scoping(self):
        """Test that functions with multiple parameters maintain proper scoping."""
        self.stacker.stack.clear()
        self.stacker.eval("{a b c} {a b * c +} $calc defun")
        result = self.stacker.eval("2 3 4 calc")
        self.assertEqual(result[-1], 10)  # 2*3 + 4 = 10


class TestFunctionScope(unittest.TestCase):
    """Test function definition scoping."""

    def setUp(self):
        self.stacker = Stacker()

    def test_function_calls_another_function(self):
        """Test that a function can call another function."""
        self.stacker.stack.clear()
        self.stacker.eval("{x} {x x *} $square defun")
        self.stacker.eval("{x} {x square 2 *} $double_square defun")
        result = self.stacker.eval("5 double_square")
        self.assertEqual(result[-1], 50)  # (5*5)*2 = 50

    def test_recursive_factorial(self):
        """Test recursive factorial function."""
        self.stacker.stack.clear()
        self.stacker.eval("""
            {n} {
                n 1 <=
                {1}
                {n n 1 - fact *}
                ifelse
            } $fact defun
        """)
        result = self.stacker.eval("5 fact")
        self.assertEqual(result[-1], 120)  # 5! = 120

    def test_mutual_recursion(self):
        """Test mutually recursive functions (even/odd checker)."""
        self.stacker.stack.clear()
        self.stacker.eval("""
            {n} {
                n 0 ==
                {1}
                {n 1 - is_odd}
                ifelse
            } $is_even defun
        """)
        self.stacker.eval("""
            {n} {
                n 0 ==
                {0}
                {n 1 - is_even}
                ifelse
            } $is_odd defun
        """)
        result = self.stacker.eval("4 is_even")
        self.assertEqual(result[-1], 1)  # 4 is even
        result = self.stacker.eval("5 is_even")
        self.assertEqual(result[-1], 0)  # 5 is not even
        result = self.stacker.eval("5 is_odd")
        self.assertEqual(result[-1], 1)  # 5 is odd


class TestLambdaScope(unittest.TestCase):
    """Test lambda function scoping."""

    def setUp(self):
        self.stacker = Stacker()

    def test_lambda_access_global_variable(self):
        """Test that lambda can $access global variables."""
        self.stacker.stack.clear()
        self.stacker.eval("10 $offset set")
        result = self.stacker.eval("[1 2 3] {x} {x offset +} lambda map")
        self.assertEqual(result[-1], [11, 12, 13])

    def test_lambda_parameter_shadows_global(self):
        """Test that lambda parameters $shadow global variables."""
        self.stacker.stack.clear()
        self.stacker.eval("100 $x set")
        result = self.stacker.eval("[1 2 3] {x} {x 2 *} lambda map")
        self.assertEqual(result[-1], [2, 4, 6])
        # Global x should still be 100
        result = self.stacker.eval("x")
        self.assertEqual(result[-1], 100)

    def test_lambda_in_function(self):
        """Test lambda used within a function."""
        self.stacker.stack.clear()
        self.stacker.eval("""
            {lst multiplier} {
                lst {x} {x multiplier *} lambda map
            } $multiply_list defun
        """)
        result = self.stacker.eval("[1 2 3 4] 3 multiply_list")
        self.assertEqual(result[-1], [3, 6, 9, 12])

    def test_lambda_recursive(self):
        """Test recursive lambda function."""
        self.stacker.stack.clear()
        # Recursive lambda factorial
        self.stacker.eval("""
            {n} {
                n 1 <=
                {1}
                {n n 1 - fact *}
                ifelse
            } lambda $fact set
        """)
        result = self.stacker.eval("5 fact eval")
        self.assertEqual(result[-1], 120)  # 5! = 120


class TestMacroScope(unittest.TestCase):
    """Test macro scoping behavior."""

    def setUp(self):
        self.stacker = Stacker()

    def test_macro_expansion(self):
        """Test basic macro expansion."""
        self.stacker.stack.clear()
        self.stacker.eval("{5 +} $add5 defmacro")
        result = self.stacker.eval("10 add5")
        self.assertEqual(result[-1], 15)

    def test_macro_with_global_variable(self):
        """Test macro $accessing global variables."""
        self.stacker.stack.clear()
        self.stacker.eval("100 $base set")
        self.stacker.eval("{base +} $add_base defmacro")
        result = self.stacker.eval("25 add_base")
        self.assertEqual(result[-1], 125)

    def test_macro_vs_function_scoping(self):
        """Test that macros and functions have different scoping behavior."""
        self.stacker.stack.clear()
        # Function evaluates in its own scope
        self.stacker.eval("{x} {x 2 *} $f_double defun")
        # Macro expands in caller's scope
        self.stacker.eval("{2 *} $m_double defmacro")

        result = self.stacker.eval("5 f_double")
        self.assertEqual(result[-1], 10)
        result = self.stacker.eval("5 m_double")
        self.assertEqual(result[-1], 10)


class TestComplexScopeScenarios(unittest.TestCase):
    """Test complex scoping scenarios."""

    def setUp(self):
        self.stacker = Stacker()

    def test_deep_recursion_scope_isolation(self):
        """Test that deep recursion maintains scope isolation."""
        self.stacker.stack.clear()
        # Sum from 1 to n
        self.stacker.eval("""
            {n} {
                n 0 <=
                {0}
                {n n 1 - sum_to +}
                ifelse
            } $sum_to defun
        """)
        result = self.stacker.eval("10 sum_to")
        self.assertEqual(result[-1], 55)  # 1+2+3+...+10 = 55

    def test_function_calls_with_different_arguments(self):
        """Test that function calls with different arguments maintain independence."""
        self.stacker.stack.clear()
        self.stacker.eval("""
            {base exp} {
                exp 0 ==
                {1}
                {base base exp 1 - power *}
                ifelse
            } $power defun
        """)
        result = self.stacker.eval("2 3 power")
        self.assertEqual(result[-1], 8)  # 2^3 = 8
        result = self.stacker.eval("3 2 power")
        self.assertEqual(result[-1], 9)  # 3^2 = 9
        result = self.stacker.eval("5 0 power")
        self.assertEqual(result[-1], 1)  # 5^0 = 1

    def test_multiple_functions_same_parameter_names(self):
        """Test multiple functions with same parameter names don't interfere."""
        self.stacker.stack.clear()
        self.stacker.eval("{x} {x 10 +} $add10 defun")
        self.stacker.eval("{x} {x 20 +} $add20 defun")
        self.stacker.eval("{x} {x 30 +} $add30 defun")

        result = self.stacker.eval("5 add10")
        self.assertEqual(result[-1], 15)
        result = self.stacker.eval("5 add20")
        self.assertEqual(result[-1], 25)
        result = self.stacker.eval("5 add30")
        self.assertEqual(result[-1], 35)

    def test_scope_with_loops(self):
        """Test scoping behavior with loops."""
        self.stacker.stack.clear()
        self.stacker.eval("0 $total set")
        self.stacker.eval("""
            [1 2 3 4 5] $i {
                total i + $total set
            } dolist
        """)
        result = self.stacker.eval("total")
        self.assertEqual(result[-1], 15)

    def test_constants_accessible_in_functions(self):
        """Test that built-in constants are accessible in functions."""
        self.stacker.stack.clear()
        self.stacker.eval("{r} {r r * pi *} $circle_area defun")
        result = self.stacker.eval("1 circle_area")
        # Should be approximately pi
        self.assertAlmostEqual(result[-1], 3.141592653589793, places=10)


class TestGlobalOperator(unittest.TestCase):
    """Test global operator behavior."""

    def setUp(self):
        self.stacker = Stacker()
        self.script_mode = ScriptMode(self.stacker)

    def test_basic_global_declaration(self):
        """Test $that global operator sets variable $in global scope."""
        script_content = """
0 $counter global
counter 1 + $counter global
counter
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            self.assertEqual(self.stacker.stack[-1], 1)
        finally:
            os.unlink(temp_file)

    def test_global_update_from_function(self):
        """Test $that global variables can be updated from functions."""
        script_content = """
0 $counter global

{x} {
    counter 1 + $counter global
    x counter *
} multiply_with_count defun

10 multiply_with_count
counter
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            self.assertEqual(self.stacker.stack[-1], 1)  # counter should be 1
        finally:
            os.unlink(temp_file)

    def test_global_multiple_function_calls(self):
        """Test global variable persists across multiple function calls."""
        script_content = """
0 $counter global

{} {
    counter 1 + $counter global
    counter
} increment defun

increment drop
increment drop
increment drop
counter
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            self.assertEqual(self.stacker.stack[-1], 3)
        finally:
            os.unlink(temp_file)

    def test_global_from_nested_function(self):
        """Test that nested functions can access and modify globals."""
        script_content = """
0 $value global

{} {
    {x} {
        x $value global
        value
    } set_value defun

    42 set_value drop
    value
} outer defun

outer
value
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            self.assertEqual(self.stacker.stack[-1], 42)
        finally:
            os.unlink(temp_file)


class TestSetVsGlobal(unittest.TestCase):
    """Tests for set operator behavior with existing vs new variables."""

    def setUp(self):
        self.stacker = Stacker()
        self.script_mode = ScriptMode(self.stacker)

    def test_set_updates_existing_global(self):
        """Test that set updates an $existing global variable."""
        script_content = """
10 x set

{} {
    20 x set
    x
} update defun

update
x
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # x should be updated to 20
            self.assertEqual(self.stacker.stack[-1], 20)
        finally:
            os.unlink(temp_file)

    def test_set_creates_local_if_not_exists(self):
        """Test that set creates local variable if it doesn't exist."""
        script_content = """
{} {
    42 newvar set
    newvar
} create_local defun

create_local
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # newvar should not exist $in global scope
            self.assertNotIn('newvar', self.stacker.variables._local)
        finally:
            os.unlink(temp_file)

    def test_set_vs_global_difference(self):
        """Test the difference between set $and global operators."""
        script_content = """
0 a set
0 b set

{} {
    10 a set
    20 $b global
    b
} modify defun

modify
a
b
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # a was updated with set (updates existing)
            self.assertEqual(self.stacker.stack[-2], 10)
            # b was updated $with global
            self.assertEqual(self.stacker.stack[-1], 20)
        finally:
            os.unlink(temp_file)


class TestLoopVariableScope(unittest.TestCase):
    """Tests for loop variable scope behavior."""

    def setUp(self):
        self.stacker = Stacker()
        self.script_mode = ScriptMode(self.stacker)

    def test_do_loop_variable_is_local(self):
        """Test that do loop variables are local to the loop."""
        script_content = """
999 i set

0 5 $i {
    i
} do

i
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # Loop should produce 0,1,2,3,4,5
            # Check a few values
            stack_list = list(self.stacker.stack)
            self.assertIn(0, stack_list[:-1])
            self.assertIn(5, stack_list[:-1])
            # Global i should still be 999
            self.assertEqual(stack_list[-1], 999)
        finally:
            os.unlink(temp_file)

    def test_dolist_loop_variable_is_local(self):
        """Test that dolist loop variables are local to the loop."""
        script_content = """
999 item set

[10 20 30] $item {
    item
} dolist

item
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # Should have 10, 20, 30 from loop
            stack_list = list(self.stacker.stack)
            self.assertIn(10, stack_list[:-1])
            self.assertIn(20, stack_list[:-1])
            self.assertIn(30, stack_list[:-1])
            # Global item should still be 999
            self.assertEqual(stack_list[-1], 999)
        finally:
            os.unlink(temp_file)

    def test_accessing_global_from_loop(self):
        """Test that loops can access and $modify global variables."""
        script_content = """
0 $sum global

1 5 $i {
    sum i + $sum global
} do

sum
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # sum should be 1+2+3+4+5 = 15
            self.assertEqual(self.stacker.stack[-1], 15)
        finally:
            os.unlink(temp_file)

    def test_nested_loops_with_same_variable_name(self):
        """Test nested loops with same variable name."""
        script_content = """
0 1 $i {
    10 11 $i {
        i
    } do
} do
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # Each outer loop iteration should run inner loop twice
            # Inner loop produces 10, 11 for each outer iteration
            # Total: 10, 11, 10, 11
            stack_list = list(self.stacker.stack)
            self.assertEqual(len(stack_list), 4)
            self.assertEqual(stack_list[0], 10)
            self.assertEqual(stack_list[1], 11)
        finally:
            os.unlink(temp_file)

    def test_loop_updating_existing_variable_with_set(self):
        """Test that loop can update existing variables with set operator."""
        script_content = """
0 total set

1 5 $i {
    total i + total set
} do

total
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # total should be 1+2+3+4+5 = 15
            self.assertEqual(self.stacker.stack[-1], 15)
        finally:
            os.unlink(temp_file)


class TestRecursiveWithGlobal(unittest.TestCase):
    """Tests for recursive functions $using global variables."""

    def setUp(self):
        self.stacker = Stacker()
        self.script_mode = ScriptMode(self.stacker)

    def test_recursive_function_with_global_counter(self):
        """Test recursive function that $uses global counter."""
        script_content = """
0 $count global

{n} {
    count 1 + $count global
    n 1 <= {
        1
    } {
        n n 1 - factorial *
    } ifelse
} factorial defun

5 factorial
count
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # 5! = 120
            self.assertEqual(self.stacker.stack[-2], 120)
            # count should be 5 (one increment per recursive call)
            self.assertEqual(self.stacker.stack[-1], 5)
        finally:
            os.unlink(temp_file)

    def test_recursive_with_global_accumulator(self):
        """Test recursive function that accumulates $in global variable."""
        script_content = """
0 $acc global

{n} {
    n 0 <= {
        acc
    } {
        acc n + $acc global
        n 1 - sum_recursive
    } ifelse
} sum_recursive defun

10 sum_recursive
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # 10+9+8+...+1 = 55
            self.assertEqual(self.stacker.stack[-1], 55)
        finally:
            os.unlink(temp_file)


class TestComplexGlobalScenarios(unittest.TestCase):
    """Tests for complex scenarios $mixing global, local, and set."""

    def setUp(self):
        self.stacker = Stacker()
        self.script_mode = ScriptMode(self.stacker)

    def test_mixed_global_local_set(self):
        """Test $mixing global, local, and set in complex scenario."""
        script_content = """
0 $a global
0 b set

{} {
    10 $a global
    20 b set
    30 c set
    0
} modify defun

modify drop
a
b
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # a was $set globally
            self.assertEqual(self.stacker.stack[-2], 10)
            # b was updated (it existed)
            self.assertEqual(self.stacker.stack[-1], 20)
            # c should not $exist globally
            self.assertNotIn('c', self.stacker.variables._local)
        finally:
            os.unlink(temp_file)

    def test_loop_inside_function_with_global(self):
        """Test loop variables inside function scope $with global accumulation."""
        script_content = """
0 $total global

{n} {
    1 n $i {
        total i + $total global
        0
    } do
    total
} accumulate defun

10 accumulate drop
total
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # 1+2+...+10 = 55
            self.assertEqual(self.stacker.stack[-1], 55)
        finally:
            os.unlink(temp_file)

    def test_function_modifying_global_in_loop(self):
        """Test function that $modifies global variable called in a loop."""
        script_content = """
0 $total global

{x} {
    total x + $total global
    total
} add_to_total defun

1 5 $i {
    i add_to_total drop
} do

total
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # total should be 1+2+3+4+5 = 15
            self.assertEqual(self.stacker.stack[-1], 15)
        finally:
            os.unlink(temp_file)

    def test_multiple_functions_sharing_global(self):
        """Test multiple functions sharing $same global variable."""
        script_content = """
0 $shared global

{x} {
    shared x + $shared global
    shared
} add_to_shared defun

{x} {
    shared x * $shared global
    shared
} multiply_shared defun

5 add_to_shared drop
2 multiply_shared drop
shared
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # shared = 0, then 0+5=5, then 5*2=10
            self.assertEqual(self.stacker.stack[-1], 10)
        finally:
            os.unlink(temp_file)


class TestScopeEdgeCases(unittest.TestCase):
    """Tests for edge cases in scope behavior."""

    def setUp(self):
        self.stacker = Stacker()
        self.script_mode = ScriptMode(self.stacker)

    def test_parameter_shadowing_global(self):
        """Test function parameter $shadowing global variable."""
        script_content = """
999 $x global

{x} {
    x 2 *
} double defun

5 double
x
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # Function uses parameter x (5), returns 10
            self.assertEqual(self.stacker.stack[-2], 10)
            # Global x unchanged
            self.assertEqual(self.stacker.stack[-1], 999)
        finally:
            os.unlink(temp_file)

    def test_loop_variable_shadowing_global(self):
        """Test loop variable $shadowing global variable."""
        script_content = """
999 $i global

1 3 $i {
    i
} do

i
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # Loop produces 1, 2, 3
            stack_list = list(self.stacker.stack)
            self.assertIn(1, stack_list[:-1])
            self.assertIn(3, stack_list[:-1])
            # Global i should still be 999
            self.assertEqual(stack_list[-1], 999)
        finally:
            os.unlink(temp_file)

    def test_global_declaration_inside_conditional(self):
        """Test global declaration inside conditional block."""
        script_content = """
1 {
    42 $result global
    result
} {
    0 $result global
    result
} ifelse

result
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stk', delete=False) as f:
            f.write(script_content)
            temp_file = f.name

        try:
            self.script_mode.run(temp_file)
            # result should be 42 since condition is true
            self.assertEqual(self.stacker.stack[-1], 42)
        finally:
            os.unlink(temp_file)


if __name__ == "__main__":
    unittest.main()


--- stacker/test/test_error_formatter.py ---
"""Tests for the error formatter."""

import unittest
from stacker.error_formatter import ErrorFormatter, StackerErrorWithContext


class TestErrorFormatter(unittest.TestCase):
    """Test cases for error formatting."""

    def test_basic_error_format(self):
        """Test basic error formatting without source context."""
        result = ErrorFormatter.format_error(
            filename="test.stk",
            line_number=10,
            column=5,
            error_type="SyntaxError",
            message="Expected a symbol, got 0"
        )
        self.assertIn("test.stk:10:5", result)
        self.assertIn("error:", result)
        self.assertIn("Expected a symbol, got 0", result)

    def test_error_with_source_line(self):
        """Test error formatting with source code context."""
        result = ErrorFormatter.format_error(
            filename="test.stk",
            line_number=5,
            column=3,
            error_type="SyntaxError",
            message="Invalid syntax",
            source_line="0 a ="
        )
        self.assertIn("test.stk:5:3", result)
        self.assertIn("0 a =", result)
        self.assertIn("^", result)  # Caret indicator

    def test_error_with_hint(self):
        """Test error formatting with hint."""
        result = ErrorFormatter.format_error(
            filename="test.stk",
            line_number=1,
            column=1,
            error_type="SyntaxError",
            message="Expected a symbol",
            source_line="123 variable set",
            hint="Use '$variable' or 'variable' (without quotes)"
        )
        self.assertIn("hint:", result)
        self.assertIn("Use '$variable'", result)

    def test_repl_error_no_filename(self):
        """Test error formatting for REPL (no filename)."""
        result = ErrorFormatter.format_error(
            filename=None,
            line_number=None,
            column=None,
            error_type="RuntimeError",
            message="Division by zero"
        )
        self.assertIn("stacker", result)
        self.assertIn("error:", result)
        self.assertIn("Division by zero", result)

    def test_warning_format(self):
        """Test warning formatting."""
        result = ErrorFormatter.format_warning(
            filename="test.stk",
            line_number=10,
            column=5,
            message="Deprecated syntax",
            source_line="$old_syntax set",
            hint="Use 'new_syntax' instead"
        )
        self.assertIn("warning:", result)
        self.assertIn("Deprecated syntax", result)
        self.assertIn("hint:", result)

    def test_stacker_error_with_context(self):
        """Test StackerErrorWithContext exception."""
        error = StackerErrorWithContext(
            message="Undefined variable 'x'",
            error_type="UndefinedVariableError",
            filename="test.stk",
            line_number=42,
            column=10,
            source_line="x 5 +",
            hint="Define 'x' before using it"
        )

        formatted = error.format()
        self.assertIn("test.stk:42:10", formatted)
        self.assertIn("Undefined variable 'x'", formatted)
        self.assertIn("x 5 +", formatted)
        self.assertIn("hint:", formatted)

    def test_column_indicator_position(self):
        """Test that the caret indicator appears at the correct column."""
        result = ErrorFormatter.format_error(
            filename="test.stk",
            line_number=1,
            column=5,
            error_type="SyntaxError",
            message="Error at column 5",
            source_line="0 1 2 3 4"
        )
        lines = result.split('\n')
        # Find the line with the caret
        caret_line = None
        for line in lines:
            if '^' in line:
                caret_line = line
                break

        self.assertIsNotNone(caret_line)
        # The caret should be at position corresponding to column 5
        # (accounting for line number prefix)

    def test_multiline_error_context(self):
        """Test error formatting preserves context structure."""
        result = ErrorFormatter.format_error(
            filename="fibonacci.stk",
            line_number=15,
            column=12,
            error_type="StackUnderflowError",
            message="Operator `+` requires 2 arguments",
            source_line="    a b + temp =",
            hint="Ensure both 'a' and 'b' are defined"
        )

        # Check all components are present
        self.assertIn("fibonacci.stk:15:12", result)
        self.assertIn("error:", result)
        self.assertIn("a b + temp =", result)
        self.assertIn("^", result)
        self.assertIn("hint:", result)
        self.assertIn("StackUnderflowError", result)


if __name__ == "__main__":
    unittest.main()


--- stacker/test/test_loop_statement.py ---
import unittest

from stacker.stacker import Stacker


class TestUnit(unittest.TestCase):
    def test_times(self):
        stacker = Stacker()
        stacker.push(1)
        self.assertEqual(list(stacker.stack), [1])
        expr = "{dup ++} 3 times"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4])

    def test_do(self):
        stacker = Stacker()
        expr = "0 $s set 1 100 $i {s i 2 ^ + $s set} do s"
        ans = stacker.eval(expr)
        self.assertEqual(ans[-1], 338350)


--- stacker/test/test_transform.py ---
import unittest

from stacker.stacker import Stacker


class TestUnit(unittest.TestCase):
    ############################
    # enumerate
    ############################
    def test_enumerate_block(self):
        stacker = Stacker()
        ans = stacker.eval("{1 2 3} enumerate list")
        self.assertEqual(ans[-1], [(0, 1), (1, 2), (2, 3)])

    def test_enumerate_list(self):
        stacker = Stacker()
        ans = stacker.eval("[1 2 3] enumerate")
        self.assertEqual(ans[-1], [(0, 1), (1, 2), (2, 3)])

    # REMOVED: test_enumerate_tuple - () now creates code blocks, not tuples

    ############################
    # sorted
    ############################
    def test_sorted_block(self):
        stacker = Stacker()
        ans = stacker.eval("{3 1 2} sorted list")
        self.assertEqual(ans[-1], [1, 2, 3])

    def test_sorted_list(self):
        stacker = Stacker()
        ans = stacker.eval("[3 1 2] sorted")
        self.assertEqual(ans[-1], [1, 2, 3])

    # REMOVED: test_sorted_tuple - () now creates code blocks, not tuples

    ############################
    # reversed
    ############################
    def test_reversed_block(self):
        stacker = Stacker()
        ans = stacker.eval("{1 2 3} reversed list")
        self.assertEqual(ans[-1], [3, 2, 1])

    def test_reversed_list(self):
        stacker = Stacker()
        ans = stacker.eval("[1 2 3] reversed")
        self.assertEqual(ans[-1], [3, 2, 1])

    # REMOVED: test_reversed_tuple - () now creates code blocks, not tuples

    ############################
    # list
    ############################
    def test_list_block(self):
        stacker = Stacker()
        ans = stacker.eval("{1 2 3} list")
        self.assertEqual(ans[-1], [1, 2, 3])

    def test_list_list(self):
        stacker = Stacker()
        ans = stacker.eval("[1 2 3] list")
        self.assertEqual(ans[-1], [1, 2, 3])

    # REMOVED: test_list_tuple - () now creates code blocks, not tuples

    # REMOVED: All tuple operator tests - tuple operator deprecated


--- stacker/test/test_error_messages.py ---
"""
Test improved error messages and error handling.

This test suite verifies that error messages are informative and helpful.
"""

import unittest
from stacker.stacker import Stacker
from stacker.error import StackUnderflowError


class TestErrorMessages(unittest.TestCase):
    """Test error messages for various error conditions."""

    def setUp(self):
        """Set up test fixtures."""
        self.stacker = Stacker()

    def test_stack_underflow_error(self):
        """Test that StackUnderflowError is raised with operator info."""
        self.stacker.stack.clear()
        with self.assertRaises(StackUnderflowError) as context:
            self.stacker.process_expression("+")

        error_msg = str(context.exception)
        self.assertIn("+", error_msg)
        self.assertIn("2", error_msg)  # + requires 2 arguments

    def test_stack_underflow_with_partial_args(self):
        """Test stack underflow when some but not all arguments are present."""
        self.stacker.stack.clear()
        with self.assertRaises(StackUnderflowError) as context:
            self.stacker.process_expression("1 +")  # + needs 2 args, only 1 provided

        error_msg = str(context.exception)
        self.assertIn("+", error_msg)

    def test_type_error_string_number_addition(self):
        """Test type error when trying to add string and number."""
        self.stacker.stack.clear()
        with self.assertRaises(TypeError) as context:
            self.stacker.process_expression('"hello" 42 +')

        error_msg = str(context.exception)
        # Should mention the type incompatibility
        self.assertTrue(
            "concatenate" in error_msg or "incompatible" in error_msg.lower()
        )

    def test_zero_division_error(self):
        """Test division by zero error."""
        self.stacker.stack.clear()
        with self.assertRaises(ZeroDivisionError):
            self.stacker.process_expression("10 0 /")

    def test_stack_underflow_multiple_operators(self):
        """Test stack underflow with different operators."""
        # Arithmetic operators raise StackUnderflowError
        arithmetic_operators = [
            ("*", 2),
            ("-", 2),
            ("+", 2),
            ("/", 2),
        ]

        for operator, expected_args in arithmetic_operators:
            with self.subTest(operator=operator):
                self.stacker.stack.clear()
                with self.assertRaises(StackUnderflowError) as context:
                    self.stacker.process_expression(operator)

                error_msg = str(context.exception)
                self.assertIn(operator, error_msg)
                self.assertIn(str(expected_args), error_msg)

    def test_stack_operators_underflow(self):
        """Test that stack manipulation operators raise errors on underflow."""
        # Stack operators have their own error types (SwapError, DupError, etc.)
        # but they should still report underflow conditions
        from stacker.error import SwapError, DupError, RotError

        test_cases = [
            ("swap", SwapError, 2),
            ("dup", DupError, 1),
            ("rot", RotError, 3),
        ]

        for operator, error_type, min_required in test_cases:
            with self.subTest(operator=operator):
                self.stacker.stack.clear()
                with self.assertRaises(error_type):
                    self.stacker.process_expression(operator)

    def test_successful_operations_no_error(self):
        """Test that correct operations don't raise errors."""
        test_cases = [
            ("1 2 +", 3),
            ("5 3 -", 2),
            ("4 3 *", 12),
            ("10 2 /", 5),
            ('"hello" " " + "world" +', "hello world"),
        ]

        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                self.stacker.stack.clear()
                self.stacker.process_expression(expr)
                result = self.stacker.stack[-1]
                self.assertEqual(result, expected)

    def test_type_error_with_operator_info(self):
        """Test that TypeError includes operator information."""
        self.stacker.stack.clear()
        with self.assertRaises(TypeError) as context:
            self.stacker.process_expression('"text" 5 -')

        error_msg = str(context.exception)
        # Should mention the operator or the incompatibility
        self.assertTrue(
            "-" in error_msg or "incompatible" in error_msg.lower()
        )


class TestStackUnderflowErrorClass(unittest.TestCase):
    """Test the StackUnderflowError class itself."""

    def test_error_message_format(self):
        """Test that StackUnderflowError formats message correctly."""
        error = StackUnderflowError("test_op", 3)
        msg = str(error)

        self.assertIn("test_op", msg)
        self.assertIn("3", msg)
        self.assertIn("arguments", msg.lower())

    def test_error_with_different_arg_counts(self):
        """Test error messages with different argument counts."""
        test_cases = [
            ("op1", 1),
            ("op2", 2),
            ("op3", 5),
        ]

        for op, count in test_cases:
            with self.subTest(op=op, count=count):
                error = StackUnderflowError(op, count)
                msg = str(error)
                self.assertIn(op, msg)
                self.assertIn(str(count), msg)


if __name__ == "__main__":
    unittest.main()


--- stacker/test/test_defun.py ---
import unittest

from stacker.stacker import Stacker


class TestStacker(unittest.TestCase):
    def setUp(self):
        self.stacker = Stacker()

    def test_function_definition_and_call_1(self):
        self.stacker.stack.clear()
        self.stacker.eval("{x} {x 2 + x 3 * +} $f defun")
        ans = self.stacker.eval("4 f")
        self.assertEqual(ans[-1], 18)

    def test_function_definition_and_call_2(self):
        self.stacker.stack.clear()
        self.stacker.eval("{xs} {xs sum} $test_sum defun")
        ans = self.stacker.eval("[1 2 3] test_sum")
        self.assertEqual(ans[-1], 6)

    def test_function_definition_and_call_3(self):
        self.stacker.stack.clear()
        self.stacker.eval("{xs} {xs sum} $test_sum defun")
        ans = self.stacker.eval("{[4 5 6]} test_sum")
        self.assertEqual(ans[-1], 15)

    def test_function_definition_and_call_4(self):
        self.stacker.stack.clear()
        self.stacker.eval("{xs} {xs sum} $test_sum defun")
        ans = self.stacker.eval("{(7 8 9)} test_sum")
        self.assertEqual(ans[-1], 24)


--- stacker/test/test_if_else_statement.py ---
import unittest

from stacker.stacker import Stacker


class TestUnit(unittest.TestCase):
    def test_if_1(self):
        # True
        stacker = Stacker()
        expr = "true 123 if"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [123])

    def test_if_2(self):
        stacker = Stacker()
        expr = "True 123 if"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [123])

    def test_if_3(self):
        stacker = Stacker()
        expr = "-1 $x set {0 x >} {3 5 +} if"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [8])

        # False

    def test_if_4(self):
        stacker = Stacker()
        expr = "false 123 if"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [])

    def test_if_5(self):
        stacker = Stacker()
        expr = "False 123 if"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [])

    def test_if_6(self):
        stacker = Stacker()
        expr = "-1 $x set {0 x <} {3 5 +} if"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [])

    def test_if_else(self):
        # True
        stacker = Stacker()
        expr = "true 114 514 ifelse"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [114])

        stacker = Stacker()
        expr = "True 114 514 ifelse"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [114])

        stacker = Stacker()
        expr = "True {114 514 +} {810 1008 +} ifelse"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [628])

        stacker = Stacker()
        expr = "-1 $x set 0 x > {114 514 +} {810 1008 +}  ifelse"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [628])

        # False
        stacker.stack.clear()
        expr = "false 114 514 ifelse"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [514])

        stacker.stack.clear()
        expr = "False 114 514 ifelse"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [514])

        stacker = Stacker()
        expr = "False {114 514 +} {810 1008 +} ifelse"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1818])

    def test_if_error(self):
        # error
        stacker = Stacker()
        expr = "{1 +} {99} iferror"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [99])

        # no error
        stacker = Stacker()
        expr = "{1 1 +} {99} iferror"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [2])


--- stacker/test/src_test/test.stk ---
{x} {x 2 ^} $power defun
{1 +} $increment defmacro

--- stacker/test/operators/test_random_operator.py ---
"""Tests for random operators (rand, randint, uniform, dice)."""

import unittest
import random
from stacker.stacker import Stacker


class TestRandomOperators(unittest.TestCase):
    def setUp(self):
        self.stacker = Stacker()
        self.stacker.stack.clear()

    def test_rand_returns_float_between_0_and_1(self):
        """Test rand returns a float between 0 and 1."""
        random.seed(42)
        self.stacker.process_expression("rand")
        result = self.stacker.stack[-1]
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_rand_multiple_calls(self):
        """Test rand produces different values on multiple calls."""
        self.stacker.process_expression("rand rand")
        val1 = self.stacker.stack[-2]
        val2 = self.stacker.stack[-1]
        # Very unlikely to be equal (but theoretically possible)
        self.assertIsInstance(val1, float)
        self.assertIsInstance(val2, float)

    def test_randint_basic(self):
        """Test randint with basic range."""
        random.seed(42)
        self.stacker.process_expression("1 10 randint")
        result = self.stacker.stack[-1]
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 1)
        self.assertLessEqual(result, 10)

    def test_randint_same_values(self):
        """Test randint with same min and max."""
        self.stacker.process_expression("5 5 randint")
        result = self.stacker.stack[-1]
        self.assertEqual(result, 5)

    def test_randint_negative_range(self):
        """Test randint with negative range."""
        random.seed(42)
        self.stacker.process_expression("-10 -1 randint")
        result = self.stacker.stack[-1]
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, -10)
        self.assertLessEqual(result, -1)

    def test_uniform_basic(self):
        """Test uniform with basic range."""
        random.seed(42)
        self.stacker.process_expression("0.0 1.0 uniform")
        result = self.stacker.stack[-1]
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_uniform_larger_range(self):
        """Test uniform with larger range."""
        random.seed(42)
        self.stacker.process_expression("10.5 20.5 uniform")
        result = self.stacker.stack[-1]
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 10.5)
        self.assertLessEqual(result, 20.5)

    def test_uniform_negative_range(self):
        """Test uniform with negative range."""
        random.seed(42)
        self.stacker.process_expression("-5.0 -1.0 uniform")
        result = self.stacker.stack[-1]
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, -5.0)
        self.assertLessEqual(result, -1.0)

    def test_dice_1d6(self):
        """Test rolling 1 six-sided die."""
        random.seed(42)
        self.stacker.process_expression("1 6 dice")
        result = self.stacker.stack[-1]
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 1)
        self.assertLessEqual(result, 6)

    def test_dice_3d6(self):
        """Test rolling 3 six-sided dice."""
        random.seed(42)
        self.stacker.process_expression("3 6 dice")
        result = self.stacker.stack[-1]
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 3)  # minimum: 1+1+1
        self.assertLessEqual(result, 18)  # maximum: 6+6+6

    def test_dice_2d20(self):
        """Test rolling 2 twenty-sided dice."""
        random.seed(42)
        self.stacker.process_expression("2 20 dice")
        result = self.stacker.stack[-1]
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 2)  # minimum: 1+1
        self.assertLessEqual(result, 40)  # maximum: 20+20

    def test_dice_deterministic(self):
        """Test dice with seed produces consistent results."""
        random.seed(12345)
        self.stacker.process_expression("3 6 dice")
        result1 = self.stacker.stack[-1]

        self.stacker.stack.clear()
        random.seed(12345)
        self.stacker.process_expression("3 6 dice")
        result2 = self.stacker.stack[-1]

        self.assertEqual(result1, result2)


if __name__ == "__main__":
    unittest.main()


--- stacker/test/operators/test_math_operator.py ---
import unittest

from stacker.stacker import Stacker
import math
import cmath


class TestUnit(unittest.TestCase):
    def setUp(self):
        self.stacker = Stacker()

    # Power (^)
    def test_pow_int(self):
        self.stacker.process_expression("2 3 ^")
        self.assertEqual(self.stacker.stack[-1], 8)

    def test_pow_float(self):
        self.stacker.process_expression("2.0 3 ^")
        self.assertEqual(self.stacker.stack[-1], 8.0)

    def test_pow_complex(self):
        self.stacker.process_expression("2j 3 ^")
        self.assertEqual(self.stacker.stack[-1], 2j**3)

    # log
    def test_log_int(self):
        self.stacker.process_expression("4 log")
        self.assertEqual(self.stacker.stack[-1], math.log(4))

    def test_log_float(self):
        self.stacker.process_expression("8.0 log")
        self.assertEqual(self.stacker.stack[-1], math.log(8.0))

    def test_log_complex(self):
        self.stacker.process_expression("8j log")
        self.assertEqual(self.stacker.stack[-1], cmath.log(8j))

    # log2
    def test_log2_int(self):
        self.stacker.process_expression("4 log2")
        self.assertEqual(self.stacker.stack[-1], math.log2(4))

    def test_log2_float(self):
        self.stacker.process_expression("8.0 log2")
        self.assertEqual(self.stacker.stack[-1], math.log2(8.0))

    def test_log2_complex(self):
        self.stacker.process_expression("8j log2")
        self.assertEqual(self.stacker.stack[-1], cmath.log(8j, 2))

    # log10
    def test_log10_int(self):
        self.stacker.process_expression("4 log10")
        self.assertEqual(self.stacker.stack[-1], math.log10(4))

    def test_log10_float(self):
        self.stacker.process_expression("8.0 log10")
        self.assertEqual(self.stacker.stack[-1], math.log10(8.0))

    def test_log10_complex(self):
        self.stacker.process_expression("8j log10")
        self.assertEqual(self.stacker.stack[-1], cmath.log10(8j))

    # exp
    def test_exp_int(self):
        self.stacker.process_expression("3 exp")
        self.assertEqual(self.stacker.stack[-1], math.exp(3))

    def test_exp_float(self):
        self.stacker.process_expression("3.0 exp")
        self.assertEqual(self.stacker.stack[-1], math.exp(3.0))

    def test_exp_complex(self):
        self.stacker.process_expression("3j exp")
        self.assertEqual(self.stacker.stack[-1], cmath.exp(3j))

    # sin
    def test_sin_int(self):
        self.stacker.process_expression("30 sin")
        self.assertEqual(self.stacker.stack[-1], math.sin(30))

    def test_sin_float(self):
        self.stacker.process_expression("30.0 sin")
        self.assertEqual(self.stacker.stack[-1], math.sin(30.0))

    def test_sin_complex(self):
        self.stacker.process_expression("30j sin")
        self.assertEqual(self.stacker.stack[-1], cmath.sin(30j))

    # cos
    def test_cos_int(self):
        self.stacker.process_expression("45 cos")
        self.assertEqual(self.stacker.stack[-1], math.cos(45))

    def test_cos_float(self):
        self.stacker.process_expression("45.0 cos")
        self.assertEqual(self.stacker.stack[-1], math.cos(45.0))

    def test_cos_complex(self):
        self.stacker.process_expression("45j cos")
        self.assertEqual(self.stacker.stack[-1], cmath.cos(45j))

    # tan
    def test_tan_int(self):
        self.stacker.process_expression("60 tan")
        self.assertEqual(self.stacker.stack[-1], math.tan(60))

    def test_tan_float(self):
        self.stacker.process_expression("60.0 tan")
        self.assertEqual(self.stacker.stack[-1], math.tan(60.0))

    def test_tan_complex(self):
        self.stacker.process_expression("60j tan")
        self.assertEqual(self.stacker.stack[-1], cmath.tan(60j))

    # asin
    def test_asin_int(self):
        self.stacker.process_expression("0 asin")
        self.assertEqual(self.stacker.stack[-1], math.asin(0))

    def test_asin_float(self):
        self.stacker.process_expression("0.5 asin")
        self.assertEqual(self.stacker.stack[-1], math.asin(0.5))

    def test_asin_complex(self):
        self.stacker.process_expression("0.5j asin")
        self.assertEqual(self.stacker.stack[-1], cmath.asin(0.5j))

    # acos
    def test_acos_int(self):
        self.stacker.process_expression("0 acos")
        self.assertEqual(self.stacker.stack[-1], math.acos(0))

    def test_acos_float(self):
        self.stacker.process_expression("0.5 acos")
        self.assertEqual(self.stacker.stack[-1], math.acos(0.5))

    def test_acos_complex(self):
        self.stacker.process_expression("0.5j acos")
        self.assertEqual(self.stacker.stack[-1], cmath.acos(0.5j))

    # atan
    def test_atan_int(self):
        self.stacker.process_expression("0 atan")
        self.assertEqual(self.stacker.stack[-1], math.atan(0))

    def test_atan_float(self):
        self.stacker.process_expression("0.5 atan")
        self.assertEqual(self.stacker.stack[-1], math.atan(0.5))

    def test_atan_complex(self):
        self.stacker.process_expression("0.5j atan")
        self.assertEqual(self.stacker.stack[-1], cmath.atan(0.5j))

    # sinh
    def test_sinh_int(self):
        self.stacker.process_expression("0 sinh")
        self.assertEqual(self.stacker.stack[-1], math.sinh(0))

    def test_sinh_float(self):
        self.stacker.process_expression("0.5 sinh")
        self.assertEqual(self.stacker.stack[-1], math.sinh(0.5))

    def test_sinh_complex(self):
        self.stacker.process_expression("0.5j sinh")
        self.assertEqual(self.stacker.stack[-1], cmath.sinh(0.5j))

    # cosh
    def test_cosh_int(self):
        self.stacker.process_expression("0 cosh")
        self.assertEqual(self.stacker.stack[-1], math.cosh(0))

    def test_cosh_float(self):
        self.stacker.process_expression("0.5 cosh")
        self.assertEqual(self.stacker.stack[-1], math.cosh(0.5))

    def test_cosh_complex(self):
        self.stacker.process_expression("0.5j cosh")
        self.assertEqual(self.stacker.stack[-1], cmath.cosh(0.5j))

    # tanh
    def test_tanh_int(self):
        self.stacker.process_expression("0 tanh")
        self.assertEqual(self.stacker.stack[-1], math.tanh(0))

    def test_tanh_float(self):
        self.stacker.process_expression("0.5 tanh")
        self.assertEqual(self.stacker.stack[-1], math.tanh(0.5))

    def test_tanh_complex(self):
        self.stacker.process_expression("0.5j tanh")
        self.assertEqual(self.stacker.stack[-1], cmath.tanh(0.5j))

    # asinh
    def test_asinh_int(self):
        self.stacker.process_expression("0 asinh")
        self.assertEqual(self.stacker.stack[-1], math.asinh(0))

    def test_asinh_float(self):
        self.stacker.process_expression("0.5 asinh")
        self.assertEqual(self.stacker.stack[-1], math.asinh(0.5))

    def test_asinh_complex(self):
        self.stacker.process_expression("0.5j asinh")
        self.assertEqual(self.stacker.stack[-1], cmath.asinh(0.5j))

    # acosh
    def test_acosh_int(self):
        self.stacker.process_expression("1 acosh")
        self.assertEqual(self.stacker.stack[-1], math.acosh(1))

    def test_acosh_float(self):
        self.stacker.process_expression("1.5 acosh")
        self.assertEqual(self.stacker.stack[-1], math.acosh(1.5))

    def test_acosh_complex(self):
        self.stacker.process_expression("1.5j acosh")
        self.assertEqual(self.stacker.stack[-1], cmath.acosh(1.5j))

    # atanh
    def test_atanh_int(self):
        self.stacker.process_expression("0 atanh")
        self.assertEqual(self.stacker.stack[-1], math.atanh(0))

    def test_atanh_float(self):
        self.stacker.process_expression("0.5 atanh")
        self.assertEqual(self.stacker.stack[-1], math.atanh(0.5))

    def test_atanh_complex(self):
        self.stacker.process_expression("0.5j atanh")
        self.assertEqual(self.stacker.stack[-1], cmath.atanh(0.5j))

    # sqrt
    def test_sqrt_int(self):
        self.stacker.process_expression("9 sqrt")
        self.assertEqual(self.stacker.stack[-1], math.sqrt(9))

    def test_sqrt_float(self):
        self.stacker.process_expression("9.0 sqrt")
        self.assertEqual(self.stacker.stack[-1], math.sqrt(9.0))

    def test_sqrt_complex(self):
        self.stacker.process_expression("9j sqrt")
        self.assertEqual(self.stacker.stack[-1], cmath.sqrt(9j))

    # gcd
    def test_gcd(self):
        self.stacker.process_expression("4 2 gcd")
        self.assertEqual(self.stacker.stack[-1], math.gcd(4, 2))

    # lcm
    def test_lcm(self):
        self.stacker.process_expression("4 2 lcm")
        self.assertEqual(self.stacker.stack[-1], math.lcm(4, 2))

    # radians
    def test_radians(self):
        self.stacker.process_expression("30 radians")
        self.assertEqual(self.stacker.stack[-1], math.radians(30))

    # factorial
    def test_factorial(self):
        self.stacker.process_expression("4 !")
        self.assertEqual(self.stacker.stack[-1], math.factorial(4))

    # ceil
    def test_ceil(self):
        self.stacker.process_expression("3.2 ceil")
        self.assertEqual(self.stacker.stack[-1], math.ceil(3.2))

    # floor
    def test_floor(self):
        self.stacker.process_expression("3.8 floor")
        self.assertEqual(self.stacker.stack[-1], math.floor(3.8))

    # roundn
    def test_roundn(self):
        self.stacker.process_expression("3.51 1 roundn")
        self.assertEqual(self.stacker.stack[-1], round(3.51, 1))

    # round
    def test_round(self):
        self.stacker.process_expression("3.5 round")
        self.assertEqual(self.stacker.stack[-1], round(3.5))


--- stacker/test/operators/test_setting_operator.py ---
"""Tests for settings operators (disable_plugin, disable_all_plugins)."""

import unittest
from io import StringIO
from unittest.mock import patch
from stacker.stacker import Stacker


class TestSettingsOperators(unittest.TestCase):
    def setUp(self):
        self.stacker = Stacker()
        self.stacker.stack.clear()

    def test_disable_plugin_existing(self):
        """Test disabling an existing plugin."""
        # Check if there are any plugins loaded
        initial_plugins = dict(self.stacker.plugins)

        if len(initial_plugins) > 0:
            # Get first plugin name
            plugin_name = list(initial_plugins.keys())[0]

            # Disable it
            self.stacker.process_expression(f"'{plugin_name}' disable_plugin")

            # Verify it's removed
            self.assertNotIn(plugin_name, self.stacker.plugins)

    def test_disable_plugin_nonexistent(self):
        """Test disabling a non-existent plugin."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.stacker.process_expression("'nonexistent_plugin' disable_plugin")
            output = fake_out.getvalue()
            self.assertIn("not registered", output)

    def test_disable_all_plugins(self):
        """Test disabling all plugins."""
        # Store initial plugin count
        initial_count = len(self.stacker.plugins)

        # Disable all plugins
        self.stacker.process_expression("disable_all_plugins")

        # Verify all plugins are removed
        self.assertEqual(len(self.stacker.plugins), 0)
        self.assertEqual(self.stacker.plugins, {})

    def test_disable_all_plugins_when_empty(self):
        """Test disabling all plugins when none are loaded."""
        # First disable all
        self.stacker.process_expression("disable_all_plugins")
        self.assertEqual(len(self.stacker.plugins), 0)

        # Disable again (should not error)
        self.stacker.process_expression("disable_all_plugins")
        self.assertEqual(len(self.stacker.plugins), 0)

    def test_disable_plugin_does_not_affect_stack(self):
        """Test that disable_plugin doesn't modify the stack."""
        self.stacker.process_expression("1 2 3")
        initial_stack = list(self.stacker.stack)

        self.stacker.process_expression("'nonexistent' disable_plugin")

        # Stack should be unchanged
        self.assertEqual(list(self.stacker.stack), initial_stack)

    def test_disable_all_plugins_does_not_affect_stack(self):
        """Test that disable_all_plugins doesn't modify the stack."""
        self.stacker.process_expression("1 2 3")
        initial_stack = list(self.stacker.stack)

        self.stacker.process_expression("disable_all_plugins")

        # Stack should be unchanged
        self.assertEqual(list(self.stacker.stack), initial_stack)


if __name__ == "__main__":
    unittest.main()


--- stacker/test/operators/test_arith_operator.py ---
import unittest

from stacker.stacker import Stacker


class TestUnit(unittest.TestCase):
    def test_add(self):
        stacker = Stacker()
        stacker.stack.append(1)
        stacker.stack.append(2)
        expr = "+"
        # integers
        self.assertEqual(list(stacker.stack), [1, 2])
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 3)
        # floats
        stacker.stack.clear()
        stacker.stack.append(3.2)
        stacker.stack.append(4.2)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 7.4)
        # complex numbers
        stacker.stack.clear()
        stacker.stack.append(3 + 4j)
        stacker.stack.append(4 + 3j)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], (7 + 7j))
        # strings
        stacker.stack.clear()
        stacker.stack.append("abc")
        stacker.stack.append("def")
        stacker.process_expression(expr)

    def test_sub(self):
        stacker = Stacker()
        stacker.stack.append(1)
        stacker.stack.append(2)
        expr = "-"
        # integers
        self.assertEqual(list(stacker.stack), [1, 2])
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], -1)
        # floats
        stacker.stack.clear()
        stacker.stack.append(3.2)
        stacker.stack.append(4.2)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], -1.0)
        # complex numbers
        stacker.stack.clear()
        stacker.stack.append(3 + 4j)
        stacker.stack.append(4 + 3j)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], (-1 + 1j))
        # strings
        stacker.stack.clear()
        stacker.stack.append("abc")
        stacker.stack.append("def")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)

    def test_mul(self):
        stacker = Stacker()
        stacker.stack.append(1)
        stacker.stack.append(2)
        expr = "*"
        # integers
        self.assertEqual(list(stacker.stack), [1, 2])
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 2)
        # floats
        stacker.stack.clear()
        stacker.stack.append(3.2)
        stacker.stack.append(4.2)
        stacker.process_expression(expr)
        self.assertAlmostEqual(stacker.stack[-1], 13.44)
        # complex numbers
        stacker.stack.clear()
        stacker.stack.append(3 + 4j)
        stacker.stack.append(4 + 3j)
        stacker.process_expression(expr)
        self.assertAlmostEqual(stacker.stack[-1], 0 + 25j)
        # strings
        stacker.stack.clear()
        stacker.stack.append("abc")
        stacker.stack.append("def")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)

    def test_div(self):
        stacker = Stacker()
        stacker.stack.append(1)
        stacker.stack.append(2)
        expr = "/"
        # integers
        self.assertEqual(list(stacker.stack), [1, 2])
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 0.5)
        # floats
        stacker.stack.clear()
        stacker.stack.append(3.2)
        stacker.stack.append(4.2)
        stacker.process_expression(expr)
        self.assertAlmostEqual(stacker.stack[-1], 0.7619047619047619)
        # complex numbers
        stacker.stack.clear()
        stacker.stack.append(3 + 4j)
        stacker.stack.append(4 + 3j)
        stacker.process_expression(expr)
        self.assertAlmostEqual(stacker.stack[-1], 0.96 + 0.28j)
        # strings
        stacker.stack.clear()
        stacker.stack.append("abc")
        stacker.stack.append("def")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)

    def test_intdiv(self):
        stacker = Stacker()
        stacker.stack.append(1)
        stacker.stack.append(2)
        expr = "//"
        # integers
        self.assertEqual(list(stacker.stack), [1, 2])
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 0)
        # floats
        stacker.stack.clear()
        stacker.stack.append(3.2)
        stacker.stack.append(4.2)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 0.0)
        # strings
        stacker.stack.clear()
        stacker.stack.append("abc")
        stacker.stack.append("def")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)

    def test_mod(self):
        stacker = Stacker()
        stacker.stack.append(1)
        stacker.stack.append(2)
        expr = "%"
        # integers
        self.assertEqual(list(stacker.stack), [1, 2])
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 1)
        # floats
        stacker.stack.clear()
        stacker.stack.append(3.2)
        stacker.stack.append(4.2)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 3.2)
        # strings
        stacker.stack.clear()
        stacker.stack.append("abc")
        stacker.stack.append("def")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)

    def test_increment(self):
        stacker = Stacker()
        stacker.stack.append(1)
        expr = "++"
        # integers
        self.assertEqual(list(stacker.stack), [1])
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 2)
        # floats
        stacker.stack.clear()
        stacker.stack.append(3.2)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 4.2)
        # strings
        stacker.stack.clear()
        stacker.stack.append("abc")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)

    def test_decrement(self):
        stacker = Stacker()
        stacker.stack.append(1)
        expr = "--"
        # integers
        self.assertEqual(list(stacker.stack), [1])
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 0)
        # floats
        stacker.stack.clear()
        stacker.stack.append(3.2)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 2.2)
        # strings
        stacker.stack.clear()
        stacker.stack.append("abc")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)


--- stacker/test/operators/test_stack_operator.py ---
import unittest

from stacker.stacker import Stacker


class TestUnit(unittest.TestCase):
    def test_drop(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        stacker.push(3)
        self.assertEqual(list(stacker.stack), [1, 2, 3])
        expr = "drop"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 2])

    def test_dup(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        stacker.push(3)
        self.assertEqual(list(stacker.stack), [1, 2, 3])
        expr = "dup"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 3])

    def test_dup2(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        stacker.push(3)
        self.assertEqual(list(stacker.stack), [1, 2, 3])
        expr = "dup2"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 2, 3])

    def test_dupn(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        stacker.push(3)
        self.assertEqual(list(stacker.stack), [1, 2, 3])
        expr = "2 dupn"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 2, 3])

    def test_swap(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        stacker.push(3)
        stacker.push(4)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4])
        expr = "swap"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 2, 4, 3])

    def test_over(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        stacker.push(3)
        stacker.push(4)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4])
        expr = "over"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4, 3])

    def test_roll(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        stacker.push(3)
        stacker.push(4)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4])
        expr = "4 roll"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [2, 3, 4, 1])

    # def test_pluck(self):
    #     stacker = Stacker()
    #     stacker.push(1)
    #     stacker.push(2)
    #     stacker.push(3)
    #     stacker.push(4)
    #     self.assertEqual(list(stacker.stack), [1, 2, 3, 4])
    #     expr = "1 pluck"
    #     stacker.process_expression(expr)
    #     self.assertEqual(list(stacker.stack), [1, 3, 4, 2])

    def test_insert(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        stacker.push(3)
        stacker.push(4)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4])
        expr = "1 5 ins"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 5, 4])

    def test_rev(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        stacker.push(3)
        stacker.push(4)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4])
        expr = "rev"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [4, 3, 2, 1])

    def test_rot(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        stacker.push(3)
        stacker.push(4)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4])
        expr = "rot"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 3, 4, 2])
        expr = "rot"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 4, 2, 3])

    def test_unrot(self):
        """Move the top element to the third position."""
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        stacker.push(3)
        stacker.push(4)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4])
        expr = "unrot"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 4, 2, 3])

    def test_pick(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        stacker.push(3)
        stacker.push(4)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4])
        expr = "1 pick"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4, 4])
        expr = "5 6"
        stacker.process_expression(expr)
        expr = "2 pick"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4, 4, 5, 6, 5])
        expr = "-1 pick"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4, 4, 5, 6, 5, 1])
        expr = "-2 pick"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4, 4, 5, 6, 5, 1, 2])
        expr = "-99 pick"
        # with self.assertRaises(IndexError):
        #     stacker.process_expression(expr)
        # expr = "99 pick"
        # with self.assertRaises(IndexError):
        #     stacker.process_expression(expr)

    def test_count(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        stacker.push(3)
        stacker.push("A")
        stacker.push("B")
        stacker.push("C")
        self.assertEqual(list(stacker.stack), [1, 2, 3, "A", "B", "C"])
        expr = "'A' count"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 2, 3, "A", "B", "C", 1])

    def test_clear(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        stacker.push(3)
        stacker.push(4)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4])
        expr = "clear"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [])

    def test_nip(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        stacker.push(3)
        stacker.push(4)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4])
        expr = "nip"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 2, 4])

    def test_depth(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        stacker.push(3)
        stacker.push(4)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4])
        expr = "depth"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [1, 2, 3, 4, 4])


--- stacker/test/operators/test_logic_operator.py ---
import unittest

from stacker.stacker import Stacker


class TestUnit(unittest.TestCase):
    def test_and(self):
        stacker = Stacker()
        stacker.push(True)
        stacker.push(True)
        self.assertEqual(list(stacker.stack), [True, True])
        expr = "and"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], True)
        stacker.push(False)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], False)
        stacker.push("abc")
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], False)

    def test_or(self):
        stacker = Stacker()
        stacker.push(True)
        stacker.push(True)
        self.assertEqual(list(stacker.stack), [True, True])
        expr = "or"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], True)
        stacker.push(False)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], True)
        stacker.push("abc")
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], True)

    def test_not(self):
        stacker = Stacker()
        stacker.push(True)
        self.assertEqual(list(stacker.stack), [True])
        expr = "not"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], False)
        stacker.push(False)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], True)


--- stacker/test/operators/test_hpf_operator.py ---
import unittest

from stacker.stacker import Stacker


class TestUnit(unittest.TestCase):
    ############################
    # map
    ############################
    def test_map_block(self):
        stacker = Stacker()
        ans = stacker.eval("{1 2 3} {2 *} map list")
        self.assertEqual(ans[-1], [2, 4, 6])

    def test_map_list(self):
        stacker = Stacker()
        ans = stacker.eval("[1 2 3] {2 *} map")
        self.assertEqual(ans[-1], [2, 4, 6])

    # REMOVED: test_map_tuple - () now creates code blocks, not tuples

    ############################
    # filter
    ############################
    def test_filter_block(self):
        stacker = Stacker()
        ans = stacker.eval("{1 2 3} {2 >} filter list")
        self.assertEqual(ans[-1], [3])

    def test_filter_list(self):
        stacker = Stacker()
        ans = stacker.eval("[1 2 3] {2 >} filter")
        self.assertEqual(ans[-1], [3])

    # REMOVED: test_filter_tuple - () now creates code blocks, not tuples

    ############################
    # zip
    ############################
    def test_zip_block(self):
        stacker = Stacker()
        ans = stacker.eval("{1 2 3} {4 5 6} zip list")
        self.assertEqual(ans[-1], [(1, 4), (2, 5), (3, 6)])

    def test_zip_list(self):
        stacker = Stacker()
        ans = stacker.eval("[1 2 3] [4 5 6] zip")
        self.assertEqual(ans[-1], [(1, 4), (2, 5), (3, 6)])

    # REMOVED: test_zip_tuple - () now creates code blocks, not tuples


--- stacker/test/operators/test_system_operator.py ---
"""Tests for system operators (vars, funcs, macros, operators)."""

import unittest
from io import StringIO
from unittest.mock import patch

from stacker.stacker import Stacker


class TestSystemOperators(unittest.TestCase):
    def setUp(self):
        self.stacker = Stacker()

    def test_vars_no_variables(self):
        """Test vars when no user variables are defined."""
        # Clear stack
        self.stacker.stack.clear()

        # Only built-in constants should exist
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.stacker.process_expression("vars")
            output = fake_out.getvalue()
            # Built-in constants should be present
            self.assertIn("e =", output)
            self.assertIn("pi =", output)
            self.assertIn("true =", output)
            self.assertIn("false =", output)

    def test_vars_with_user_variables(self):
        """Test vars with user-defined variables."""
        self.stacker.stack.clear()
        self.stacker.process_expression("5 $x set")
        self.stacker.process_expression("10 $y set")
        self.stacker.process_expression("'hello' $msg set")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.stacker.process_expression("vars")
            output = fake_out.getvalue()
            self.assertIn("x = 5", output)
            self.assertIn("y = 10", output)
            self.assertIn("msg = hello", output)

    def test_funcs_no_functions(self):
        """Test funcs when no functions are defined."""
        self.stacker.stack.clear()

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.stacker.process_expression("funcs")
            output = fake_out.getvalue()
            self.assertIn("No functions defined", output)

    def test_funcs_with_user_functions(self):
        """Test funcs with user-defined functions."""
        self.stacker.stack.clear()
        self.stacker.process_expression("{x} {x x *} $square defun")
        self.stacker.process_expression("{x y} {x y +} $add defun")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.stacker.process_expression("funcs")
            output = fake_out.getvalue()
            self.assertIn("square", output)
            self.assertIn("add", output)
            self.assertIn("['x']", output)
            self.assertIn("['x', 'y']", output)

    def test_funcs_execution(self):
        """Test that defined functions actually work."""
        self.stacker.stack.clear()
        self.stacker.process_expression("{x} {x x *} $square defun")
        self.stacker.process_expression("5 square")
        self.assertEqual(self.stacker.stack[-1], 25)

    def test_macros_no_macros(self):
        """Test macros when no macros are defined."""
        self.stacker.stack.clear()

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.stacker.process_expression("macros")
            output = fake_out.getvalue()
            self.assertIn("No macros defined", output)

    def test_macros_with_user_macros(self):
        """Test macros with user-defined macros."""
        self.stacker.stack.clear()
        self.stacker.process_expression("{x} {x x *} $sqr defmacro")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.stacker.process_expression("macros")
            output = fake_out.getvalue()
            self.assertIn("sqr", output)
            # Macros display the blockstack
            self.assertIn("{", output)

    def test_operators_display(self):
        """Test operators command displays operator categories."""
        self.stacker.stack.clear()

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.stacker.process_expression("operators")
            output = fake_out.getvalue()

            # Check for major sections
            self.assertIn("Regular operators:", output)
            self.assertIn("Stack operators:", output)
            self.assertIn("Settings operators:", output)

            # Check for some specific operators
            self.assertIn("+", output)  # Arithmetic
            self.assertIn("dup", output)  # Stack
            self.assertIn("if", output)  # Control flow

    def test_operators_includes_system_operators(self):
        """Test that operators command includes system operators."""
        self.stacker.stack.clear()

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.stacker.process_expression("operators")
            output = fake_out.getvalue()

            # System operators should be listed
            self.assertIn("vars", output)
            self.assertIn("funcs", output)
            self.assertIn("macros", output)
            self.assertIn("operators", output)

    def test_vars_in_script_mode(self):
        """Test that vars works in script mode (not just REPL)."""
        # This tests that system operators are part of the language
        from stacker.runtime.exec_modes import ScriptMode
        import tempfile
        import os

        # Create a temporary script file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".stk", delete=False) as f:
            f.write("5 $x set\n")
            f.write("10 $y set\n")
            f.write("vars\n")
            script_path = f.name

        try:
            stacker = Stacker()
            script_mode = ScriptMode(stacker)

            with patch("sys.stdout", new=StringIO()) as fake_out:
                script_mode.run(script_path)
                output = fake_out.getvalue()
                self.assertIn("x = 5", output)
                self.assertIn("y = 10", output)
        finally:
            os.unlink(script_path)

    def test_vars_does_not_modify_stack(self):
        """Test that vars command does not modify the stack."""
        self.stacker.stack.clear()
        self.stacker.process_expression("1 2 3")
        self.assertEqual(list(self.stacker.stack), [1, 2, 3])

        with patch("sys.stdout", new=StringIO()):
            self.stacker.process_expression("vars")

        # Stack should remain unchanged
        self.assertEqual(list(self.stacker.stack), [1, 2, 3])

    def test_funcs_does_not_modify_stack(self):
        """Test that funcs command does not modify the stack."""
        self.stacker.stack.clear()
        self.stacker.process_expression("1 2 3")
        self.assertEqual(list(self.stacker.stack), [1, 2, 3])

        with patch("sys.stdout", new=StringIO()):
            self.stacker.process_expression("funcs")

        # Stack should remain unchanged
        self.assertEqual(list(self.stacker.stack), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()


--- stacker/test/operators/test_algebra_operator.py ---
import unittest

from stacker.stacker import Stacker


class TestUnit(unittest.TestCase):
    def test_neg(self):
        stacker = Stacker()
        stacker.stack.append(1)
        self.assertEqual(stacker.stack[-1], 1)
        expr = "neg"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], -1)
        stacker.stack.append(4.2)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], -4.2)
        stacker.stack.append("abc")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)


--- stacker/test/operators/test_special_operator.py ---
import unittest

from stacker.stacker import Stacker


class TestUnit(unittest.TestCase):
    def test_seq(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(5)
        self.assertEqual(list(stacker.stack), [1, 5])
        expr = "seq"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [[1, 2, 3, 4, 5]])
        stacker.push(1.1)
        stacker.push(4.2)
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)

    def test_len(self):
        stacker = Stacker()
        stacker.push([1, 2, 3, 4, 5])
        self.assertEqual(list(stacker.stack), [[1, 2, 3, 4, 5]])
        expr = "len"
        stacker.process_expression(expr)
        # self.assertEqual(list(stacker.stack), [[1, 2, 3, 4, 5], 5])
        self.assertEqual(list(stacker.stack), [5])

    def test_min(self):
        stacker = Stacker()
        stacker.push([1, 2, 3, 4, 5])
        self.assertEqual(list(stacker.stack), [[1, 2, 3, 4, 5]])
        expr = "min"
        stacker.process_expression(expr)
        # self.assertEqual(list(stacker.stack), [[1, 2, 3, 4, 5], 1])
        self.assertEqual(list(stacker.stack), [1])

    def test_max(self):
        stacker = Stacker()
        stacker.push([1, 2, 3, 4, 5])
        self.assertEqual(list(stacker.stack), [[1, 2, 3, 4, 5]])
        expr = "max"
        stacker.process_expression(expr)
        # self.assertEqual(list(stacker.stack), [[1, 2, 3, 4, 5], 5])
        self.assertEqual(list(stacker.stack), [5])

    def test_split_space(self):
        stacker = Stacker()
        expr = """'a b c' ' ' split"""
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), ["a", "b", "c"])

    def test_split_comma(self):
        stacker = Stacker()
        expr = """'a,b,c' ',' split"""
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), ["a", "b", "c"])

    def test_nth_list(self):
        stacker = Stacker()
        expr = "[1 2 3] 1 nth"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [[1, 2, 3], 2])

    # REMOVED: test_nth_tuple - () now creates code blocks, not tuples

    def test_nth_string(self):
        stacker = Stacker()
        expr = "'abc' 1 nth"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), ["abc", "b"])

    def test_read_from_string(self):
        stacker = Stacker()
        expr = "'3 4 +' read-from-string"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1].tokens, [3, 4, "+"])

    def test_sub(self):
        stacker = Stacker()
        expr = "5 sub"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1].tokens, [5])

    def test_subn(self):
        stacker = Stacker()
        expr = "1 2 3 3 subn"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1].tokens, [1, 2, 3])


--- stacker/test/operators/test_comparation_operator.py ---
import unittest

from stacker.stacker import Stacker


class TestUnit(unittest.TestCase):
    def test_eq(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(1)
        self.assertEqual(list(stacker.stack), [1, 1])
        expr = "=="
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], True)
        stacker.push(4.2)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], False)
        stacker.push("abc")
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], False)

    def test_ne(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(1)
        self.assertEqual(list(stacker.stack), [1, 1])
        expr = "!="
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], False)
        stacker.push(4.2)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], True)
        stacker.push("abc")
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], True)

    def test_gt(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(1)
        self.assertEqual(list(stacker.stack), [1, 1])
        expr = ">"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], False)
        stacker.push(4.2)
        stacker.push(4.1)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], True)
        stacker.push("abc")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)

    def test_lt(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(1)
        self.assertEqual(list(stacker.stack), [1, 1])
        expr = "<"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], False)
        stacker.push(4.2)
        stacker.push(4.3)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], True)
        stacker.push("abc")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)

    def test_ge(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(1)
        self.assertEqual(list(stacker.stack), [1, 1])
        expr = ">="
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], True)
        stacker.push(4.2)
        stacker.push(4.3)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], False)
        stacker.push("abc")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)

    def test_le(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(1)
        self.assertEqual(list(stacker.stack), [1, 1])
        expr = "<="
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], True)
        stacker.push(4.2)
        stacker.push(4.1)
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], False)
        stacker.push("abc")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)


--- stacker/test/operators/test_os_operator.py ---
"""Tests for OS operators (ls, cd, pwd, cat)."""

import unittest
import tempfile
import os
from io import StringIO
from unittest.mock import patch
from stacker.stacker import Stacker


class TestOSOperators(unittest.TestCase):
    def setUp(self):
        self.stacker = Stacker()
        self.stacker.stack.clear()
        # Store original working directory
        self.original_dir = os.getcwd()
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Restore original working directory
        os.chdir(self.original_dir)
        # Clean up temporary directory
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_pwd_returns_current_directory(self):
        """Test pwd returns current working directory."""
        self.stacker.process_expression("pwd")
        result = self.stacker.stack[-1]
        self.assertEqual(result, os.getcwd())
        self.assertIsInstance(result, str)

    def test_cd_changes_directory(self):
        """Test cd changes the current directory."""
        # Change to temp directory
        self.stacker.process_expression(f"'{self.temp_dir}' cd")

        # Verify directory changed
        self.assertEqual(os.getcwd(), self.temp_dir)

    def test_cd_and_pwd(self):
        """Test cd followed by pwd."""
        self.stacker.process_expression(f"'{self.temp_dir}' cd")
        self.stacker.process_expression("pwd")

        result = self.stacker.stack[-1]
        self.assertEqual(result, self.temp_dir)

    def test_ls_lists_files(self):
        """Test ls lists files in current directory."""
        # Change to temp directory and create some files
        os.chdir(self.temp_dir)
        open(os.path.join(self.temp_dir, "file1.txt"), "w").close()
        open(os.path.join(self.temp_dir, "file2.txt"), "w").close()

        self.stacker.process_expression("ls")
        result = self.stacker.stack[-1]

        self.assertIsInstance(result, list)
        self.assertIn("file1.txt", result)
        self.assertIn("file2.txt", result)

    def test_ls_empty_directory(self):
        """Test ls in an empty directory."""
        # Create an empty subdirectory
        empty_dir = os.path.join(self.temp_dir, "empty")
        os.makedirs(empty_dir)
        os.chdir(empty_dir)

        self.stacker.process_expression("ls")
        result = self.stacker.stack[-1]

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_cat_prints_file_content(self):
        """Test cat prints file content."""
        # Create a test file
        filepath = os.path.join(self.temp_dir, "cat_test.txt")
        with open(filepath, "w") as f:
            f.write("Hello from cat")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.stacker.process_expression(f"'{filepath}' cat")
            output = fake_out.getvalue()
            self.assertIn("Hello from cat", output)

    def test_cat_multiline_content(self):
        """Test cat with multiline content."""
        filepath = os.path.join(self.temp_dir, "multiline_cat.txt")
        content = "Line 1\nLine 2\nLine 3"
        with open(filepath, "w") as f:
            f.write(content)

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.stacker.process_expression(f"'{filepath}' cat")
            output = fake_out.getvalue()
            self.assertEqual(output.strip(), content)

    def test_ls_does_not_modify_stack_before_operation(self):
        """Test ls pushes result to stack."""
        self.stacker.process_expression("1 2 3")
        initial_length = len(self.stacker.stack)

        self.stacker.process_expression("ls")

        # ls should push result, so stack length should increase
        self.assertEqual(len(self.stacker.stack), initial_length + 1)

    def test_cd_does_not_push_to_stack(self):
        """Test cd does not push result to stack."""
        self.stacker.process_expression("1 2 3")
        initial_length = len(self.stacker.stack)

        self.stacker.process_expression(f"'{self.temp_dir}' cd")

        # cd consumes the path from stack but doesn't push result
        self.assertEqual(len(self.stacker.stack), initial_length)

    def test_pwd_pushes_to_stack(self):
        """Test pwd pushes current directory to stack."""
        self.stacker.process_expression("1 2 3")
        initial_length = len(self.stacker.stack)

        self.stacker.process_expression("pwd")

        # pwd should push result
        self.assertEqual(len(self.stacker.stack), initial_length + 1)


if __name__ == "__main__":
    unittest.main()


--- stacker/test/operators/test_base_operator.py ---
import unittest

from stacker.stacker import Stacker


class TestUnit(unittest.TestCase):
    def test_bin(self):
        stacker = Stacker()
        stacker.stack.append(1)
        stacker.stack.append(2)
        self.assertEqual(list(stacker.stack), [1, 2])
        expr = "bin"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], "0b10")
        stacker.stack.append(4.2)
        with self.assertRaises(ValueError):
            stacker.process_expression(expr)
        stacker.stack.append("abc")
        with self.assertRaises(ValueError):
            stacker.process_expression(expr)

    def test_oct(self):
        stacker = Stacker()
        stacker.stack.append(1)
        stacker.stack.append(2)
        self.assertEqual(list(stacker.stack), [1, 2])
        expr = "oct"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], "0o2")
        stacker.stack.append(4.2)
        with self.assertRaises(ValueError):
            stacker.process_expression(expr)
        stacker.stack.append("abc")
        with self.assertRaises(ValueError):
            stacker.process_expression(expr)

    def test_dec(self):
        stacker = Stacker()
        stacker.stack.append(1)
        stacker.stack.append(2)
        self.assertEqual(list(stacker.stack), [1, 2])
        expr = "dec"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 2)
        stacker.stack.append(4.2)
        with self.assertRaises(ValueError):
            stacker.process_expression(expr)
        stacker.stack.append("abc")
        with self.assertRaises(ValueError):
            stacker.process_expression(expr)

    def test_hex(self):
        stacker = Stacker()
        stacker.stack.append(1)
        stacker.stack.append(255)
        self.assertEqual(list(stacker.stack), [1, 255])
        expr = "hex"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], "0xff")
        stacker.stack.append(4.2)
        with self.assertRaises(ValueError):
            stacker.process_expression(expr)
        stacker.stack.append("abc")
        with self.assertRaises(ValueError):
            stacker.process_expression(expr)


--- stacker/test/operators/test_file_operator.py ---
"""Tests for file operators (write-to-file, read-from-file, append-to-file, read-lines, file-exists)."""

import unittest
import tempfile
import os
from stacker.stacker import Stacker


class TestFileOperators(unittest.TestCase):
    def setUp(self):
        self.stacker = Stacker()
        self.stacker.stack.clear()
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up temporary directory
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def get_temp_file(self, name="test.txt"):
        """Get a path to a temporary file."""
        return os.path.join(self.temp_dir, name)

    def test_write_to_file_basic(self):
        """Test writing to a file."""
        filepath = self.get_temp_file("write_test.txt")
        self.stacker.process_expression(f"'Hello World' '{filepath}' write-to-file")

        # Verify file was created and contains the content
        self.assertTrue(os.path.exists(filepath))
        with open(filepath, "r") as f:
            content = f.read()
        self.assertEqual(content, "Hello World")

    def test_write_to_file_number(self):
        """Test writing a number to a file."""
        filepath = self.get_temp_file("number_test.txt")
        self.stacker.process_expression(f"42 '{filepath}' write-to-file")

        with open(filepath, "r") as f:
            content = f.read()
        self.assertEqual(content, "42")

    def test_write_to_file_overwrites(self):
        """Test that write-to-file overwrites existing content."""
        filepath = self.get_temp_file("overwrite_test.txt")

        # Write first content
        self.stacker.process_expression(f"'First' '{filepath}' write-to-file")

        # Write second content (should overwrite)
        self.stacker.process_expression(f"'Second' '{filepath}' write-to-file")

        with open(filepath, "r") as f:
            content = f.read()
        self.assertEqual(content, "Second")

    def test_read_from_file_basic(self):
        """Test reading from a file."""
        filepath = self.get_temp_file("read_test.txt")

        # Create a file with content
        with open(filepath, "w") as f:
            f.write("Hello from file")

        self.stacker.process_expression(f"'{filepath}' read-from-file")
        result = self.stacker.stack[-1]
        self.assertEqual(result, "Hello from file")

    def test_read_from_file_multiline(self):
        """Test reading multiline content from a file."""
        filepath = self.get_temp_file("multiline_test.txt")

        content = "Line 1\nLine 2\nLine 3"
        with open(filepath, "w") as f:
            f.write(content)

        self.stacker.process_expression(f"'{filepath}' read-from-file")
        result = self.stacker.stack[-1]
        self.assertEqual(result, content)

    def test_append_to_file_basic(self):
        """Test appending to a file."""
        filepath = self.get_temp_file("append_test.txt")

        # Write initial content
        self.stacker.process_expression(f"'Hello' '{filepath}' write-to-file")

        # Append content
        self.stacker.process_expression(f"' World' '{filepath}' append-to-file")

        with open(filepath, "r") as f:
            content = f.read()
        self.assertEqual(content, "Hello World")

    def test_append_to_file_creates_if_not_exists(self):
        """Test that append creates file if it doesn't exist."""
        filepath = self.get_temp_file("new_append_test.txt")

        self.stacker.process_expression(f"'New content' '{filepath}' append-to-file")

        self.assertTrue(os.path.exists(filepath))
        with open(filepath, "r") as f:
            content = f.read()
        self.assertEqual(content, "New content")

    def test_append_to_file_multiple_times(self):
        """Test appending to a file multiple times."""
        filepath = self.get_temp_file("multi_append_test.txt")

        self.stacker.process_expression(f"'A' '{filepath}' write-to-file")
        self.stacker.process_expression(f"'B' '{filepath}' append-to-file")
        self.stacker.process_expression(f"'C' '{filepath}' append-to-file")

        with open(filepath, "r") as f:
            content = f.read()
        self.assertEqual(content, "ABC")

    def test_read_lines_basic(self):
        """Test reading lines from a file."""
        filepath = self.get_temp_file("lines_test.txt")

        with open(filepath, "w") as f:
            f.write("Line 1\nLine 2\nLine 3")

        self.stacker.process_expression(f"'{filepath}' read-lines")
        result = self.stacker.stack[-1]
        self.assertEqual(result, ["Line 1", "Line 2", "Line 3"])

    def test_read_lines_empty_file(self):
        """Test reading lines from an empty file."""
        filepath = self.get_temp_file("empty_test.txt")

        with open(filepath, "w") as f:
            f.write("")

        self.stacker.process_expression(f"'{filepath}' read-lines")
        result = self.stacker.stack[-1]
        self.assertEqual(result, [])

    def test_read_lines_single_line(self):
        """Test reading a single line from a file."""
        filepath = self.get_temp_file("single_line_test.txt")

        with open(filepath, "w") as f:
            f.write("Only one line")

        self.stacker.process_expression(f"'{filepath}' read-lines")
        result = self.stacker.stack[-1]
        self.assertEqual(result, ["Only one line"])

    def test_read_lines_trailing_newline(self):
        """Test reading lines with trailing newline."""
        filepath = self.get_temp_file("trailing_newline_test.txt")

        with open(filepath, "w") as f:
            f.write("Line 1\nLine 2\n")

        self.stacker.process_expression(f"'{filepath}' read-lines")
        result = self.stacker.stack[-1]
        # Trailing newline should result in 2 lines, not 3
        self.assertEqual(result, ["Line 1", "Line 2"])

    def test_file_exists_true(self):
        """Test file-exists returns true for existing file."""
        filepath = self.get_temp_file("exists_test.txt")

        # Create the file
        with open(filepath, "w") as f:
            f.write("content")

        self.stacker.process_expression(f"'{filepath}' file-exists")
        result = self.stacker.stack[-1]
        self.assertTrue(result)

    def test_file_exists_false(self):
        """Test file-exists returns false for non-existent file."""
        filepath = self.get_temp_file("nonexistent.txt")

        self.stacker.process_expression(f"'{filepath}' file-exists")
        result = self.stacker.stack[-1]
        self.assertFalse(result)

    def test_file_exists_directory(self):
        """Test file-exists with a directory."""
        # The temp_dir should exist
        self.stacker.process_expression(f"'{self.temp_dir}' file-exists")
        result = self.stacker.stack[-1]
        self.assertTrue(result)

    def test_write_read_roundtrip(self):
        """Test writing and reading back produces same content."""
        filepath = self.get_temp_file("roundtrip_test.txt")
        test_content = "Test content for roundtrip"

        self.stacker.process_expression(f"'{test_content}' '{filepath}' write-to-file")
        self.stacker.stack.clear()
        self.stacker.process_expression(f"'{filepath}' read-from-file")

        result = self.stacker.stack[-1]
        self.assertEqual(result, test_content)


if __name__ == "__main__":
    unittest.main()


--- stacker/test/operators/test_list_operator.py ---
import unittest

from stacker.stacker import Stacker


class TestUnit(unittest.TestCase):
    def test_seq(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(5)
        self.assertEqual(list(stacker.stack), [1, 5])
        expr = "seq"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [[1, 2, 3, 4, 5]])

    def test_len(self):
        stacker = Stacker()
        stacker.push([1, 2, 3, 4, 5])
        self.assertEqual(list(stacker.stack), [[1, 2, 3, 4, 5]])
        expr = "len"
        stacker.process_expression(expr)
        # self.assertEqual(list(stacker.stack), [[1, 2, 3, 4, 5], 5])
        self.assertEqual(list(stacker.stack), [5])

    def test_min(self):
        stacker = Stacker()
        stacker.push([1, 2, 3, 4, 5])
        self.assertEqual(list(stacker.stack), [[1, 2, 3, 4, 5]])
        expr = "min"
        stacker.process_expression(expr)
        # self.assertEqual(list(stacker.stack), [[1, 2, 3, 4, 5], 1])
        self.assertEqual(list(stacker.stack), [1])

    def test_max(self):
        stacker = Stacker()
        stacker.push([1, 2, 3, 4, 5])
        self.assertEqual(list(stacker.stack), [[1, 2, 3, 4, 5]])
        expr = "max"
        stacker.process_expression(expr)
        # self.assertEqual(list(stacker.stack), [[1, 2, 3, 4, 5], 5])
        self.assertEqual(list(stacker.stack), [5])

    def test_sum(self):
        stacker = Stacker()
        stacker.push([1, 2, 3, 4, 5])
        self.assertEqual(list(stacker.stack), [[1, 2, 3, 4, 5]])
        expr = "sum"
        stacker.process_expression(expr)
        self.assertEqual(list(stacker.stack), [15])


--- stacker/test/operators/test_bitwise_operator.py ---
import unittest

from stacker.stacker import Stacker


class TestUnit(unittest.TestCase):
    def test_band(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        self.assertEqual(list(stacker.stack), [1, 2])
        expr = "band"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 0)
        stacker.push(4.2)
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)
        stacker.push("abc")
        stacker.push("edf")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)

    def test_bor(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        self.assertEqual(list(stacker.stack), [1, 2])
        expr = "bor"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 3)
        stacker.push(4.2)
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)
        stacker.push("abc")
        stacker.push("edf")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)

    def test_bxor(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        self.assertEqual(list(stacker.stack), [1, 2])
        expr = "bxor"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 3)
        stacker.push(4.2)
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)
        stacker.push("abc")
        stacker.push("edf")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)

    def test_bnot(self):
        stacker = Stacker()
        stacker.push(1)
        self.assertEqual(list(stacker.stack), [1])
        expr = "~"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], -2)
        stacker.push(4.2)
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)
        stacker.push("abc")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)

    def test_lshift(self):
        stacker = Stacker()
        stacker.push(1)
        stacker.push(2)
        self.assertEqual(list(stacker.stack), [1, 2])
        expr = "<<"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 4)
        stacker.push(4.2)
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)
        stacker.push("abc")
        stacker.push("edf")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)

    def test_rshift(self):
        stacker = Stacker()
        stacker.push(8)
        stacker.push(2)
        self.assertEqual(list(stacker.stack), [8, 2])
        expr = ">>"
        stacker.process_expression(expr)
        self.assertEqual(stacker.stack[-1], 2)
        stacker.push(4.2)
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)
        stacker.push("abc")
        stacker.push("edf")
        with self.assertRaises(TypeError):
            stacker.process_expression(expr)


--- stacker/test/plugin_test/test_matrix_operations_plugin.py ---
# import unittest

# import numpy as np

# from stacker.plugins import matrix
# from stacker.stacker import Stacker


# class TestMatrixOperationsPlugin(unittest.TestCase):
#     def setUp(self):
#         self.stacker = Stacker()
#         matrix.setup(self.stacker)

#     # ================================
#     # +
#     # ================================
#     def test_matrix_add(self):
#         expression = "[1 2; 3 4] [5 6; 7 8] +"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         # expected_result = (a + b).tolist()
#         expected_result = [[6, 8], [10, 12]]
#         self.assertEqual(self.stacker.stack[-1], expected_result)
#         print("\n")
#         print(f"expression: {expression}")
#         print(f"result: {self.stacker.stack[-1]}")

#     def test_scalar_add(self):
#         expression = "1 2 +"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         expected_result = 3
#         self.assertEqual(self.stacker.stack[-1], expected_result)

#     # ================================
#     # -
#     # ================================
#     def test_matrix_sub(self):
#         expression = "[1 2; 3 4] [5 6; 7 8] -"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         # expected_result = (a - b).tolist()
#         expected_result = [[-4, -4], [-4, -4]]
#         self.assertEqual(self.stacker.stack[-1], expected_result)

#     def test_scalar_sub(self):
#         expression = "1 2 -"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         expected_result = -1
#         self.assertEqual(self.stacker.stack[-1], expected_result)

#     # ================================
#     # *
#     # ================================
#     def test_matrix_mul(self):
#         expression = "[1 2; 3 4] [5 6; 7 8] *"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         # expected_result = (np.dot(a, b)).tolist()
#         expected_result = [[19, 22], [43, 50]]
#         self.assertEqual(self.stacker.stack[-1], expected_result)
#         print("\n")
#         print(f"expression: {expression}")
#         print(f"result: {self.stacker.stack[-1]}")

#     def test_scalar_mul(self):
#         expression = "4 2 *"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         expected_result = 8
#         self.assertEqual(self.stacker.stack[-1], expected_result)

#     # ================================
#     # .*
#     # ================================
#     def test_elementwise_mul(self):
#         expression = "[1 2; 3 4] [5 6; 7 8] .*"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         # expected_result = np.multiply(a, b).tolist()
#         expected_result = [[5, 12], [21, 32]]
#         self.assertEqual(self.stacker.stack[-1], expected_result)
#         print("\n")
#         print(f"expression: {expression}")
#         print(f"result: {self.stacker.stack[-1]}")

#     def test_scalar_elementwise_mul(self):
#         expression = "2 3 .*"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         expected_result = 6
#         self.assertEqual(self.stacker.stack[-1], expected_result)

#     # ================================
#     # /
#     # ================================
#     def test_matrix_div(self):
#         a = [[1, 2], [3, 4]]
#         b = [[5, 6], [7, 8]]
#         expression = "[1 2; 3 4] [5 6; 7 8] /"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         # expected_result = np.divide(a, b).tolist()
#         result = self.stacker.stack[-1]
#         expected_result = [[3.0, -2.0], [2.0, -1.0]]

#         for sub_list1, sub_list2 in zip(result, expected_result):
#             for a, b in zip(sub_list1, sub_list2):
#                 self.assertAlmostEqual(a, b, places=5)

#         # self.assertEqual(self.stacker.stack[-1], expected_result)
#         print("\n")
#         print(f"expression: {expression}")
#         print(f"result: {self.stacker.stack[-1]}")

#     def test_scalar_div(self):
#         expression = "4 2 /"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         expected_result = 2
#         self.assertEqual(self.stacker.stack[-1], expected_result)

#     # ================================
#     # ./
#     # ================================
#     def test_elementwise_div(self):
#         a = [[1, 2], [3, 4]]
#         b = [[5, 6], [7, 8]]
#         expression = "[1 2; 3 4] [5 6; 7 8] ./"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         result = self.stacker.stack[-1]
#         expected_result = [[0.2000, 0.3333], [0.4286, 0.5000]]

#         for sub_list1, sub_list2 in zip(result, expected_result):
#             for a, b in zip(sub_list1, sub_list2):
#                 self.assertAlmostEqual(a, b, delta=1e-4)

#         print("\n")
#         print(f"expression: {expression}")
#         print(f"result: {self.stacker.stack[-1]}")

#     def test_scalar_elementwise_div(self):
#         expression = "4 2 ./"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         expected_result = 2
#         self.assertEqual(self.stacker.stack[-1], expected_result)

#     # def test_elementwise_div_inv(self):
#     #     a = [[1, 2], [3, 4]]
#     #     b = [[5, 6], [7, 8]]
#     #     expression = "[1 2; 3 4] [5 6; 7 8] .\\"
#     #     self.stacker.stack.clear()
#     #     self.stacker.process_expression(expression)
#     #     expected_result = np.divide(b, a).tolist()
#     #     self.assertEqual(self.stacker.stack[-1], expected_result)
#     #     print("\n")
#     #     print(f"expression: {expression}")
#     #     print(f"result: {self.stacker.stack[-1]}")

#     # ================================
#     # ^
#     # ================================
#     def test_matrix_power(self):
#         expression = "[1 2; 3 4] 3 ^"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         self.stacker.process_expression(expression)
#         result = self.stacker.stack[-1]
#         expected_result = [[37, 54], [81, 118]]
#         self.assertEqual(result, expected_result)

#     def test_scalar_power(self):
#         expression = "2 3 ^"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         result = self.stacker.stack[-1]
#         expected_result = 8
#         self.assertEqual(result, expected_result)

#     # ================================
#     # .^
#     # ================================
#     def test_elementwise_power(self):
#         expression = "[1 2; 3 4] 3 .^"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         result = self.stacker.stack[-1]
#         expected_result = [[1, 8], [27, 64]]
#         self.assertEqual(result, expected_result)
#         print("\n")
#         print(f"expression: {expression}")
#         print(f"result: {self.stacker.stack[-1]}")

#     def test_scalar_elementwise_power(self):
#         expression = "2 3 .^"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         result = self.stacker.stack[-1]
#         expected_result = 8
#         self.assertEqual(result, expected_result)

#     def test_matrix_transpose(self):
#         a = [[1, 2], [3, 4]]
#         expression = "[1 2; 3 4] '"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         expected_result = np.transpose(a).tolist()
#         self.assertEqual(self.stacker.stack[-1], expected_result)
#         print("\n")
#         print(f"expression: {expression}")
#         print(f"result: {self.stacker.stack[-1]}")

#     def test_matrix_inverse(self):
#         a = [[1, 2], [3, 4]]
#         expression = "[1 2; 3 4] inv"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         expected_result = np.linalg.inv(a).tolist()
#         self.assertEqual(self.stacker.stack[-1], expected_result)
#         print("\n")
#         print(f"expression: {expression}")
#         print(f"result: {self.stacker.stack[-1]}")

#     def test_matrix_determinant(self):
#         a = [[1, 2], [3, 4]]
#         expression = "[1 2; 3 4] det"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         expected_result = np.linalg.det(a)
#         self.assertEqual(self.stacker.stack[-1], expected_result)
#         print("\n")
#         print(f"expression: {expression}")
#         print(f"result: {self.stacker.stack[-1]}")

#     def test_matrix_rank(self):
#         a = [[1, 2], [3, 4]]
#         expression = "[1 2; 3 4] rank"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         expected_result = np.linalg.matrix_rank(a)
#         self.assertEqual(self.stacker.stack[-1], expected_result)
#         print("\n")
#         print(f"expression: {expression}")
#         print(f"result: {self.stacker.stack[-1]}")

#     def test_matrix_trace(self):
#         a = [[1, 2], [3, 4]]
#         expression = "[1 2; 3 4] trace"
#         self.stacker.stack.clear()
#         self.stacker.process_expression(expression)
#         expected_result = np.trace(a).tolist()
#         self.assertEqual(self.stacker.stack[-1], expected_result)
#         print("\n")
#         print(f"expression: {expression}")
#         print(f"result: {self.stacker.stack[-1]}")


# if __name__ == "__main__":
#     unittest.main()


--- stacker/test/syntax/test_block.py ---
import unittest

from stacker.stacker import Stacker


class TestUnit(unittest.TestCase):
    def test_enmpty_block(self):
        stacker = Stacker()
        expr = "{}"
        try:
            stacker.process_expression(expr)
            assert True
        except Exception as e:
            assert False, e

        assert stacker.stack[0].tokens == []

    def test_block(self):
        stacker = Stacker()
        expr = "{0}"
        ans = stacker.eval(expr)
        assert ans[-1].tokens == [0]

    def test_block2(self):
        stacker = Stacker()
        expr = "{0 1 +}"
        ans = stacker.eval(expr)
        assert ans[-1].tokens == [0, 1, "+"]

    # Tests for () code blocks (Lisp-style syntax)
    def test_paren_empty_block(self):
        stacker = Stacker()
        expr = "()"
        try:
            stacker.process_expression(expr)
            assert True
        except Exception as e:
            assert False, e
        assert stacker.stack[0].tokens == []

    def test_paren_code_block(self):
        stacker = Stacker()
        expr = "(1 2 +)"
        ans = stacker.eval(expr)
        # Should create code block, not execute
        # Check that the last element is a code block with the right tokens
        assert hasattr(ans[-1], "tokens")
        assert ans[-1].tokens == [1, 2, "+"]

    def test_paren_block_execution(self):
        stacker = Stacker()
        ans = stacker.eval("(1 2 +) eval")
        # Should execute and return 3
        self.assertEqual(ans[-1], 3)

    def test_paren_with_if_statement(self):
        stacker = Stacker()
        stacker.process_expression("true (10 20 +) if")
        # Should execute block when condition is true
        self.assertEqual(list(stacker.stack), [30])

    def test_paren_lisp_style_function(self):
        stacker = Stacker()
        stacker.eval("(x y) (x y *) $mul defun")
        ans = stacker.eval("3 4 mul")
        self.assertEqual(ans[-1], 12)

    def test_paren_brace_interchangeable(self):
        stacker = Stacker()
        ans1 = stacker.eval("(1 2 +) eval")
        stacker2 = Stacker()
        ans2 = stacker2.eval("{1 2 +} eval")
        # () and {} should behave identically
        self.assertEqual(ans1[-1], ans2[-1])

    def test_bracket_type_display_paren(self):
        """Test that () code blocks display with () not {}"""
        stacker = Stacker()
        ans = stacker.eval("(1 2 +)")
        # Should display as () not {}
        self.assertEqual(str(ans[-1]), "(1 2 +)")

    def test_bracket_type_display_brace(self):
        """Test that {} code blocks display with {} not ()"""
        stacker = Stacker()
        ans = stacker.eval("{3 4 *}")
        # Should display as {} not ()
        self.assertEqual(str(ans[-1]), "{3 4 *}")

    def test_nested_bracket_type_preservation(self):
        """Test that nested blocks preserve their bracket types"""
        stacker = Stacker()

        # Test ({...})
        ans = stacker.eval("({1 2 +})")
        self.assertEqual(str(ans[-1]), "({1 2 +})")

        # Test {(...)}
        stacker.stack.clear()
        ans = stacker.eval("{(5 6 -)}")
        self.assertEqual(str(ans[-1]), "{(5 6 -)}")


--- stacker/test/syntax/test_token.py ---
import unittest

from stacker.stacker import Stacker
from stacker import error
from stacker.error import (
    # StackUnderflowError,
    # StackerSyntaxError,
    UndefinedSymbolError,
    # UnexpectedTokenError,
)


class TestUnit(unittest.TestCase):
    ############################
    # valid list
    ############################
    def test_valid_list(self):
        stacker = Stacker()
        ans = stacker.eval("[1 2 3]")
        self.assertEqual(ans[-1], [1, 2, 3])

    def test_valid_list_2(self):
        stacker = Stacker()
        ans = stacker.eval("[1 2 3; 4 5 6]")
        self.assertEqual(ans[-1], [[1, 2, 3], [4, 5, 6]])

    def test_valid_list_3(self):
        stacker = Stacker()
        ans = stacker.eval("[1 2 3; 4 5 6; 7 8 9]")
        self.assertEqual(ans[-1], [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    def test_valid_list_4(self):
        stacker = Stacker()
        ans = stacker.eval("[[1 2 3; 4 5 6]; [7 8 9; 10 11 12]]")
        self.assertEqual(ans[-1], [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])

    ############################
    # Invalid list
    ############################
    def test_invalid_list(self):
        stacker = Stacker()
        # Undefined symbols in lists are now treated as UndefinedSymbol objects
        # They only raise errors when used in operations
        result = stacker.eval("[x]")
        # The list should contain an UndefinedSymbol
        from stacker.engine.data_type import UndefinedSymbol

        self.assertIsInstance(result[-1][0], UndefinedSymbol)

    def test_invalid_list_2(self):
        stacker = Stacker()
        # Undefined symbols in lists are now treated as UndefinedSymbol objects
        result = stacker.eval("[x y]")
        from stacker.engine.data_type import UndefinedSymbol

        self.assertIsInstance(result[-1][0], UndefinedSymbol)
        self.assertIsInstance(result[-1][1], UndefinedSymbol)

    ############################
    # valid tuple
    ############################

    # REMOVED: All tuple tests - () now creates code blocks, not tuples
    # test_valid_tuple, test_valid_tuple_2, test_valid_tuple_3, test_valid_tuple_4
    # test_invalid_tuple, test_invalid_tuple_2

    ############################
    # Undefined symbol
    ############################
    def test_undefined_symbol(self):
        stacker = Stacker()
        # Undefined symbols are now treated as UndefinedSymbol objects
        from stacker.engine.data_type import UndefinedSymbol

        result = stacker.eval("x")
        self.assertIsInstance(result[-1], UndefinedSymbol)
        # But using them in operations should raise an error
        with self.assertRaises(error.UndefinedSymbolError):
            stacker.eval("x 5 +")


--- stacker/test/runtime/exec_modes/test_execution_modes.py ---
"""Tests for execution modes (ExecutionMode, ScriptMode, CommandLineMode)."""

import unittest
import tempfile
import os
from io import StringIO
from unittest.mock import patch

from stacker.stacker import Stacker
from stacker.runtime.exec_modes import ExecutionMode, ScriptMode, CommandLineMode


class TestExecutionMode(unittest.TestCase):
    """Test the base ExecutionMode class."""

    def setUp(self):
        self.rpn_calculator = Stacker()
        self.exec_mode = ExecutionMode(self.rpn_calculator)

    def test_initialization(self):
        """Test ExecutionMode initialization."""
        self.assertEqual(self.exec_mode.rpn_calculator, self.rpn_calculator)
        self.assertTrue(self.exec_mode.color_print)
        self.assertFalse(self.exec_mode.debug)

    def test_debug_mode(self):
        """Test debug mode activation."""
        self.assertFalse(self.exec_mode.debug)
        self.exec_mode.debug_mode()
        self.assertTrue(self.exec_mode.debug)

    def test_disp(self):
        """Test stack display."""
        self.rpn_calculator.stack.clear()
        self.rpn_calculator.process_expression("1 2 3")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.exec_mode.disp()
            output = fake_out.getvalue()
            self.assertIn("1", output)
            self.assertIn("2", output)
            self.assertIn("3", output)

    def test_disp_all_variables(self):
        """Test variable display."""
        self.rpn_calculator.stack.clear()
        self.rpn_calculator.process_expression("5 $x set")
        self.rpn_calculator.process_expression("10 $y set")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.exec_mode.disp_all_variables()
            output = fake_out.getvalue()
            self.assertIn("x = 5", output)
            self.assertIn("y = 10", output)

    def test_disp_ans(self):
        """Test answer display."""
        self.rpn_calculator.stack.clear()
        self.rpn_calculator.process_expression("1 2 +")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.exec_mode.disp_ans()
            output = fake_out.getvalue()
            self.assertIn("3", output)

    def test_disp_ans_empty_stack(self):
        """Test answer display with empty stack."""
        self.rpn_calculator.stack.clear()

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.exec_mode.disp_ans()
            output = fake_out.getvalue()
            self.assertEqual(output, "")

    def test_execute_stacker_dotfile(self):
        """Test executing a dotfile."""
        # Create a temporary dotfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".stk", delete=False) as f:
            f.write("5 $x set\n")
            f.write("10 $y set\n")
            dotfile_path = f.name

        try:
            self.rpn_calculator.stack.clear()
            self.exec_mode.execute_stacker_dotfile(dotfile_path)

            # Variables should be set
            self.assertEqual(self.rpn_calculator.variables["x"], 5)
            self.assertEqual(self.rpn_calculator.variables["y"], 10)
        finally:
            os.unlink(dotfile_path)

    def test_execute_stacker_dotfile_with_multiline(self):
        """Test executing a dotfile with multiline expressions."""
        # Create a temporary dotfile with multiline expressions
        with tempfile.NamedTemporaryFile(mode="w", suffix=".stk", delete=False) as f:
            f.write("[1 2 3;\n")
            f.write("4 5 6]\n")
            f.write("$matrix set\n")
            dotfile_path = f.name

        try:
            self.rpn_calculator.stack.clear()
            self.exec_mode.execute_stacker_dotfile(dotfile_path)

            # Matrix should be set (with semicolon, it creates nested list)
            self.assertEqual(
                self.rpn_calculator.variables["matrix"], [[1, 2, 3], [4, 5, 6]]
            )
        finally:
            os.unlink(dotfile_path)


class TestScriptMode(unittest.TestCase):
    """Test ScriptMode execution."""

    def setUp(self):
        self.rpn_calculator = Stacker()
        self.script_mode = ScriptMode(self.rpn_calculator)

    def test_script_mode_basic(self):
        """Test basic script execution."""
        # Create a temporary script
        with tempfile.NamedTemporaryFile(mode="w", suffix=".stk", delete=False) as f:
            f.write("1 2 +\n")
            f.write("3 *\n")
            script_path = f.name

        try:
            self.rpn_calculator.stack.clear()
            self.script_mode.run(script_path)

            # Result should be (1+2)*3 = 9
            self.assertEqual(self.rpn_calculator.stack[-1], 9)
        finally:
            os.unlink(script_path)

    def test_script_mode_with_variables(self):
        """Test script execution with variables."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".stk", delete=False) as f:
            f.write("5 $x set\n")
            f.write("10 $y set\n")
            f.write("x y +\n")
            script_path = f.name

        try:
            self.rpn_calculator.stack.clear()
            self.script_mode.run(script_path)

            # Result should be 5+10 = 15
            self.assertEqual(self.rpn_calculator.stack[-1], 15)
        finally:
            os.unlink(script_path)

    def test_script_mode_with_functions(self):
        """Test script execution with function definitions."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".stk", delete=False) as f:
            f.write("{x} {x x *} $square defun\n")
            f.write("5 square\n")
            script_path = f.name

        try:
            self.rpn_calculator.stack.clear()
            self.script_mode.run(script_path)

            # Result should be 5^2 = 25
            self.assertEqual(self.rpn_calculator.stack[-1], 25)
        finally:
            os.unlink(script_path)

    def test_script_mode_uses_system_operators(self):
        """Test that script mode can use system operators."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".stk", delete=False) as f:
            f.write("5 $x set\n")
            f.write("vars\n")
            script_path = f.name

        try:
            with patch("sys.stdout", new=StringIO()) as fake_out:
                self.script_mode.run(script_path)
                output = fake_out.getvalue()
                self.assertIn("x = 5", output)
        finally:
            os.unlink(script_path)


class TestCommandLineMode(unittest.TestCase):
    """Test CommandLineMode execution."""

    def setUp(self):
        self.rpn_calculator = Stacker()
        self.cmd_mode = CommandLineMode(self.rpn_calculator)

    def test_commandline_mode_basic(self):
        """Test basic command line execution."""
        self.rpn_calculator.stack.clear()
        # CommandLineMode uses eval() which returns result but clears stack
        # This is intentional behavior for command-line mode
        self.cmd_mode.run("1 2 +")
        # Result is computed, but for testing we check it doesn't error
        # The actual output would be handled by __main__.py
        # Just verify it doesn't error
        result = self.rpn_calculator.eval("1 2 +")
        self.assertEqual(result[-1], 3)

    def test_commandline_mode_with_variables(self):
        """Test command line mode with variables."""
        self.rpn_calculator.stack.clear()

        # First set a variable (using process_expression to keep it in state)
        self.rpn_calculator.process_expression("5 $x set")
        # Then use it via eval
        result = self.rpn_calculator.eval("x 10 +")
        self.assertEqual(result[-1], 15)

    def test_commandline_mode_multiple_expressions(self):
        """Test command line mode with multiple expressions."""
        self.rpn_calculator.stack.clear()
        result = self.rpn_calculator.eval("1 2 + 3 * 4 +")
        # (1+2)*3+4 = 13
        self.assertEqual(result[-1], 13)

    def test_commandline_mode_uses_system_operators(self):
        """Test that command line mode can use system operators."""
        self.rpn_calculator.stack.clear()

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.cmd_mode.run("5 $x set")
            # Clear previous output
            fake_out.truncate(0)
            fake_out.seek(0)

            self.cmd_mode.run("vars")
            output = fake_out.getvalue()
            self.assertIn("x = 5", output)


if __name__ == "__main__":
    unittest.main()


--- stacker/test/runtime/exec_modes/test_repl_mode.py ---
import unittest
from io import StringIO
from unittest.mock import patch
from stacker.runtime.exec_modes.repl_mode import ReplMode
from stacker.stacker import Stacker


class TestReplMode(unittest.TestCase):
    def setUp(self):
        self.rpn_calculator = Stacker()
        self.repl_mode = ReplMode(self.rpn_calculator)

    @patch("stacker.runtime.exec_modes.repl_mode.version")
    def test_get_version(self, mock_version):
        mock_version.return_value = "1.0.0"
        rpn_calculator = Stacker()
        repl_mode = ReplMode(rpn_calculator)
        result = repl_mode.get_version()
        self.assertEqual(result, "1.0.0")
        mock_version.assert_called_once_with("pystacker")

    def test_repl_mode_initialization(self):
        """Test that ReplMode initializes with correct default settings."""
        self.assertTrue(self.repl_mode.disp_stack_mode)
        self.assertTrue(self.repl_mode.disp_logo_mode)
        self.assertFalse(self.repl_mode.disp_ans_mode)

    def test_repl_commands_list(self):
        """Test that REPL commands list is properly initialized."""
        self.assertIn("help", self.repl_mode.repl_commands)
        self.assertIn("about", self.repl_mode.repl_commands)
        self.assertIn("delete_history", self.repl_mode.repl_commands)

    def test_get_completer(self):
        """Test that get_completer returns expected words."""
        completer_words = self.repl_mode.get_completer()

        # Should include REPL commands
        self.assertIn("help", completer_words)
        self.assertIn("about", completer_words)

        # Should include operators
        self.assertIn("+", completer_words)
        self.assertIn("dup", completer_words)

        # Should include system operators
        self.assertIn("vars", completer_words)
        self.assertIn("funcs", completer_words)

    def test_handle_repl_command_help(self):
        """Test that help command is handled correctly."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            result = self.repl_mode._handle_repl_command("help")
            self.assertTrue(result)
            output = fake_out.getvalue()
            self.assertIn("operators", output.lower())

    def test_handle_repl_command_about(self):
        """Test that about command is handled correctly."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            result = self.repl_mode._handle_repl_command("about")
            self.assertTrue(result)
            output = fake_out.getvalue()
            self.assertIn("Stacker", output)

    def test_handle_repl_command_enable_disp_stack(self):
        """Test enable_disp_stack command."""
        self.repl_mode.disp_stack_mode = False
        result = self.repl_mode._handle_repl_command("enable_disp_stack")
        self.assertTrue(result)
        self.assertTrue(self.repl_mode.disp_stack_mode)

    def test_handle_repl_command_disable_disp_stack(self):
        """Test disable_disp_stack command."""
        self.repl_mode.disp_stack_mode = True
        result = self.repl_mode._handle_repl_command("disable_disp_stack")
        self.assertTrue(result)
        self.assertFalse(self.repl_mode.disp_stack_mode)

    def test_handle_repl_command_enable_disp_logo(self):
        """Test enable_disp_logo command."""
        self.repl_mode.disp_logo_mode = False
        result = self.repl_mode._handle_repl_command("enable_disp_logo")
        self.assertTrue(result)
        self.assertTrue(self.repl_mode.disp_logo_mode)

    def test_handle_repl_command_disable_disp_logo(self):
        """Test disable_disp_logo command."""
        self.repl_mode.disp_logo_mode = True
        result = self.repl_mode._handle_repl_command("disable_disp_logo")
        self.assertTrue(result)
        self.assertFalse(self.repl_mode.disp_logo_mode)

    def test_handle_repl_command_enable_disp_ans(self):
        """Test enable_disp_ans command."""
        self.repl_mode.disp_ans_mode = False
        result = self.repl_mode._handle_repl_command("enable_disp_ans")
        self.assertTrue(result)
        self.assertTrue(self.repl_mode.disp_ans_mode)

    def test_handle_repl_command_disable_disp_ans(self):
        """Test disable_disp_ans command."""
        self.repl_mode.disp_ans_mode = True
        result = self.repl_mode._handle_repl_command("disable_disp_ans")
        self.assertTrue(result)
        self.assertFalse(self.repl_mode.disp_ans_mode)

    def test_handle_repl_command_case_insensitive(self):
        """Test that REPL commands are case-insensitive."""
        with patch("sys.stdout", new=StringIO()):
            # Test uppercase
            result1 = self.repl_mode._handle_repl_command("HELP")
            self.assertTrue(result1)

            # Test mixed case
            result2 = self.repl_mode._handle_repl_command("HeLp")
            self.assertTrue(result2)

    def test_handle_repl_command_not_a_command(self):
        """Test that non-commands return False."""
        result = self.repl_mode._handle_repl_command("1 2 +")
        self.assertFalse(result)

        result = self.repl_mode._handle_repl_command("not_a_command")
        self.assertFalse(result)

    def test_handle_repl_command_delete_history(self):
        """Test delete_history command."""
        with patch(
            "stacker.runtime.exec_modes.repl_mode.delete_history"
        ) as mock_delete:
            result = self.repl_mode._handle_repl_command("delete_history")
            self.assertTrue(result)
            mock_delete.assert_called_once()

    def test_cmd_help_includes_system_operators(self):
        """Test that help command includes system operators."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.repl_mode._cmd_help()
            output = fake_out.getvalue()

            # Should include system operators section
            self.assertIn("System operators:", output)
            self.assertIn("vars", output)
            self.assertIn("funcs", output)
            self.assertIn("macros", output)
            self.assertIn("operators", output)


if __name__ == "__main__":
    unittest.main()


--- stacker/test/runtime/exec_modes/lib/test_ui_tools.py ---
import unittest
from unittest.mock import patch, mock_open
from stacker.lib.ui_tools import disp_logo, disp_about, disp_help, delete_history


class TestUITools(unittest.TestCase):
    @patch("stacker.lib.ui_tools.files")
    @patch("stacker.lib.ui_tools.colored")
    def test_disp_logo(self, mock_colored, mock_files):
        mock_file = mock_open(read_data=b"Line1\nLine2\nLine3\nLine4\nLine5\nLine6\n")
        mock_files.return_value.joinpath.return_value.open = mock_file

        with patch("builtins.print") as mock_print:
            disp_logo()
            self.assertEqual(mock_print.call_count, 7)  # 6 lines + 1 empty line
            self.assertTrue(mock_colored.called)

    @patch("stacker.lib.ui_tools.files")
    def test_disp_about(self, mock_files):
        mock_file = mock_open(read_data=b"About message")
        mock_files.return_value.joinpath.return_value.open = mock_file

        with patch("builtins.print") as mock_print:
            disp_about()
            mock_print.assert_called_once_with("About message")

    @patch("stacker.lib.ui_tools.files")
    def test_disp_help(self, mock_files):
        mock_file = mock_open(read_data=b"Help message")
        mock_files.return_value.joinpath.return_value.open = mock_file

        with patch("builtins.print") as mock_print:
            disp_help()
            mock_print.assert_called_once_with("Help message")

    @patch("stacker.lib.ui_tools.history_file_path")
    def test_delete_history(self, mock_history_file_path):
        mock_history_file_path.exists.return_value = True

        delete_history()
        mock_history_file_path.unlink.assert_called_once()

        mock_history_file_path.exists.return_value = False
        delete_history()
        with patch.object(
            mock_history_file_path, "unlink", wraps=mock_history_file_path.unlink
        ) as mock_unlink:
            delete_history()
            mock_unlink.assert_not_called()


if __name__ == "__main__":
    unittest.main()


--- stacker/.vscode-extension/package.json ---
{
  "name": "stacker-language",
  "displayName": "Stacker Language Support",
  "description": "Syntax highlighting for Stacker stack-based programming language",
  "version": "0.1.0",
  "publisher": "stacker",
  "repository": {
    "type": "git",
    "url": "https://github.com/remokasu/stacker.git"
  },
  "engines": {
    "vscode": "^1.50.0"
  },
  "categories": [
    "Programming Languages"
  ],
  "contributes": {
    "languages": [
      {
        "id": "stacker",
        "aliases": ["Stacker", "stacker"],
        "extensions": [".stk"],
        "configuration": "./language-configuration.json",
        "icon": {
          "light": "./icon.png",
          "dark": "./icon.png"
        }
      }
    ],
    "grammars": [
      {
        "language": "stacker",
        "scopeName": "source.stacker",
        "path": "./syntaxes/stacker.tmLanguage.json"
      }
    ]
  }
}


--- stacker/.vscode-extension/language-configuration.json ---
{
  "comments": {
    "lineComment": "#"
  },
  "brackets": [
    ["{", "}"],
    ["[", "]"],
    ["(", ")"]
  ],
  "autoClosingPairs": [
    { "open": "{", "close": "}" },
    { "open": "[", "close": "]" },
    { "open": "(", "close": ")" },
    { "open": "\"", "close": "\"" },
    { "open": "'", "close": "'" }
  ],
  "surroundingPairs": [
    ["{", "}"],
    ["[", "]"],
    ["(", ")"],
    ["\"", "\""],
    ["'", "'"]
  ],
  "folding": {
    "markers": {
      "start": "^\\s*\\{",
      "end": "^\\s*\\}"
    }
  },
  "indentationRules": {
    "increaseIndentPattern": "^\\s*\\{[^}]*$",
    "decreaseIndentPattern": "^\\s*\\}"
  }
}


--- stacker/.vscode-extension/syntaxes/stacker.tmLanguage.json ---
{
  "$schema": "https://raw.githubusercontent.com/martinring/tmlanguage/master/tmlanguage.json",
  "name": "Stacker",
  "patterns": [
    {
      "include": "#comments"
    },
    {
      "include": "#strings"
    },
    {
      "include": "#numbers"
    },
    {
      "include": "#constants"
    },
    {
      "include": "#operators"
    },
    {
      "include": "#control-flow"
    },
    {
      "include": "#function-definition"
    },
    {
      "include": "#variables"
    },
    {
      "include": "#blocks"
    }
  ],
  "repository": {
    "comments": {
      "patterns": [
        {
          "name": "comment.line.number-sign.stacker",
          "match": "#.*$"
        }
      ]
    },
    "strings": {
      "patterns": [
        {
          "name": "string.quoted.double.stacker",
          "begin": "\"",
          "end": "\"",
          "patterns": [
            {
              "name": "constant.character.escape.stacker",
              "match": "\\\\."
            }
          ]
        },
        {
          "name": "string.quoted.single.stacker",
          "begin": "'",
          "end": "'",
          "patterns": [
            {
              "name": "constant.character.escape.stacker",
              "match": "\\\\."
            }
          ]
        }
      ]
    },
    "numbers": {
      "patterns": [
        {
          "name": "constant.numeric.complex.stacker",
          "match": "\\b[0-9]+\\.?[0-9]*[+-][0-9]+\\.?[0-9]*j\\b"
        },
        {
          "name": "constant.numeric.hex.stacker",
          "match": "\\b0x[0-9a-fA-F]+\\b"
        },
        {
          "name": "constant.numeric.octal.stacker",
          "match": "\\b0o[0-7]+\\b"
        },
        {
          "name": "constant.numeric.binary.stacker",
          "match": "\\b0b[01]+\\b"
        },
        {
          "name": "constant.numeric.float.stacker",
          "match": "\\b[0-9]+\\.[0-9]+([eE][+-]?[0-9]+)?\\b"
        },
        {
          "name": "constant.numeric.integer.stacker",
          "match": "\\b[0-9]+\\b"
        }
      ]
    },
    "constants": {
      "patterns": [
        {
          "name": "constant.language.stacker",
          "match": "\\b(true|false|pi|e|tau|inf|nan)\\b"
        }
      ]
    },
    "operators": {
      "patterns": [
        {
          "name": "keyword.operator.arithmetic.stacker",
          "match": "\\b(\\+{1,2}|\\-{1,2}|\\*|\\/\\/?|\\%|\\^|neg|inc|dec|intdiv|!)\\b"
        },
        {
          "name": "keyword.operator.comparison.stacker",
          "match": "\\b(==|!=|<=|>=|<|>|eq|ne|le|ge|lt|gt)\\b"
        },
        {
          "name": "keyword.operator.logical.stacker",
          "match": "\\b(and|or|not|&&|\\|\\|)\\b"
        },
        {
          "name": "keyword.operator.bitwise.stacker",
          "match": "\\b(band|bor|bxor|bnot|~|lshift|rshift|<<|>>)\\b"
        },
        {
          "name": "keyword.operator.stack.stacker",
          "match": "\\b(dup|dup2|dupn|drop|drop2|dropn|swap|over|rot|unrot|pick|roll|nip|depth|clear|rev|insert|ins|count|disp)\\b"
        },
        {
          "name": "keyword.operator.math.stacker",
          "match": "\\b(sin|cos|tan|asin|acos|atan|sinh|cosh|tanh|asinh|acosh|atanh|sqrt|exp|log|log2|log10|pow|abs|ceil|floor|round|roundn|factorial|gcd|lcm|radians|random|randint|uniform|frac|dice)\\b"
        },
        {
          "name": "keyword.operator.aggregate.stacker",
          "match": "\\b(sum|min|max|len|any|all)\\b"
        },
        {
          "name": "keyword.operator.list.stacker",
          "match": "\\b(seq|map|filter|reduce|fold|zip|enumerate|sort|sorted|reverse|reversed|tolist|list)\\b"
        },
        {
          "name": "keyword.operator.conversion.stacker",
          "match": "\\b(bin|oct|dec|hex|float|int)\\b"
        },
        {
          "name": "keyword.operator.io.stacker",
          "match": "\\b(echo|print|printc|input|read)\\b"
        },
        {
          "name": "keyword.operator.file.stacker",
          "match": "\\b(write-to-file|append-to-file|read-from-file|read-lines|file-exists)\\b"
        },
        {
          "name": "keyword.operator.eval.stacker",
          "match": "\\b(eval|include|sub|subn|expand|read-from-string)\\b"
        }
      ]
    },
    "control-flow": {
      "patterns": [
        {
          "name": "keyword.control.stacker",
          "match": "\\b(if|ifelse|iferror|do|dolist|times|break)\\b"
        }
      ]
    },
    "function-definition": {
      "patterns": [
        {
          "name": "keyword.control.definition.stacker",
          "match": "\\b(defun|defmacro|lambda)\\b"
        }
      ]
    },
    "variables": {
      "patterns": [
        {
          "name": "variable.other.dollar.stacker",
          "match": "\\$[a-zA-Z_][a-zA-Z0-9_]*"
        },
        {
          "name": "keyword.operator.assignment.stacker",
          "match": "\\b(set|=|global)\\b"
        }
      ]
    },
    "blocks": {
      "patterns": [
        {
          "name": "meta.block.stacker",
          "begin": "\\{",
          "end": "\\}",
          "patterns": [
            {
              "include": "$self"
            }
          ]
        },
        {
          "name": "meta.list.stacker",
          "begin": "\\[",
          "end": "\\]",
          "patterns": [
            {
              "include": "$self"
            }
          ]
        }
      ]
    }
  },
  "scopeName": "source.stacker"
}


--- stacker/stacker/reserved.py ---
__BREAK__ = "\b"
__TRANSPOSE__ = "\T"


--- stacker/stacker/__init__.py ---
from __future__ import annotations

import os

from stacker import constant, error, stacker
from stacker.stacker import Stacker

__all__ = ["stacker", "error", "constant", "include", "Stacker"]

# リソースフォルダへのパスを取得する
resource_path = os.path.join(os.path.dirname(__file__), "data")

plugins_path = os.path.join(os.path.dirname(__file__), "plugins")

# モジュールにパスを追加する
__path__.append(resource_path)
__path__.append(plugins_path)


--- stacker/stacker/constant.py ---
from __future__ import annotations

import math


constants = {
    "e": math.e,
    "pi": math.pi,
    "phi": (1 + math.sqrt(5)) / 2,
    "tau": math.tau,
    "nan": math.nan,
    "inf": float("inf"),
    "true": True,
    "false": False,
    "null": None,
}


--- stacker/stacker/error_formatter.py ---
"""
Error formatter for Stacker with Clang-style output.

Provides rich, visual error messages with:
- File location and line number
- Source code context
- Visual indicators (arrows, highlighting)
- Color-coded severity levels
"""

from __future__ import annotations
from typing import Optional
import sys


class ErrorFormatter:
    """Formats error messages in a Clang-like style with visual indicators."""

    # ANSI color codes
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'

    @staticmethod
    def _supports_color() -> bool:
        """Check if the terminal supports color output."""
        return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

    @classmethod
    def format_error(
        cls,
        filename: Optional[str],
        line_number: Optional[int],
        column: Optional[int],
        error_type: str,
        message: str,
        source_line: Optional[str] = None,
        hint: Optional[str] = None
    ) -> str:
        """
        Format an error message in Clang style.

        Args:
            filename: Source file name (None for REPL)
            line_number: Line number where error occurred
            column: Column number where error occurred
            error_type: Type of error (e.g., "SyntaxError", "RuntimeError")
            message: Error message
            source_line: The source code line that caused the error
            hint: Optional hint for fixing the error

        Returns:
            Formatted error message string
        """
        use_color = cls._supports_color()
        lines = []

        # Location line: "filename:line:column: error: message"
        location_parts = []
        if filename:
            location_parts.append(f"{filename}")
        if line_number is not None:
            location_parts.append(f"{line_number}")
        if column is not None:
            location_parts.append(f"{column}")

        location = ":".join(location_parts) if location_parts else "stacker"

        if use_color:
            error_label = f"{cls.BOLD}{cls.RED}error:{cls.RESET}"
            location = f"{cls.BOLD}{location}{cls.RESET}"
        else:
            error_label = "error:"

        lines.append(f"{location}: {error_label} {message}")

        # Add error type if different from "error"
        if error_type and error_type.lower() != "error":
            if use_color:
                lines.append(f"  {cls.GRAY}[{error_type}]{cls.RESET}")
            else:
                lines.append(f"  [{error_type}]")

        # Source code context with visual indicator
        if source_line is not None and line_number is not None:
            # Line number padding
            line_num_str = str(line_number)
            padding = len(line_num_str) + 1

            if use_color:
                line_prefix = f"{cls.BLUE}{line_num_str} |{cls.RESET} "
                blank_prefix = f"{cls.BLUE}{' ' * len(line_num_str)} |{cls.RESET} "
            else:
                line_prefix = f"{line_num_str} | "
                blank_prefix = f"{' ' * len(line_num_str)} | "

            lines.append(blank_prefix)
            lines.append(f"{line_prefix}{source_line}")

            # Visual indicator (caret ^ or arrow)
            if column is not None and column > 0:
                # Adjust for line number prefix
                indicator_pos = column - 1
                spaces = ' ' * indicator_pos

                if use_color:
                    indicator = f"{blank_prefix}{spaces}{cls.BOLD}{cls.GREEN}^{cls.RESET}"
                else:
                    indicator = f"{blank_prefix}{spaces}^"

                lines.append(indicator)

        # Optional hint
        if hint:
            if use_color:
                lines.append(f"{cls.BOLD}{cls.CYAN}hint:{cls.RESET} {hint}")
            else:
                lines.append(f"hint: {hint}")

        return "\n".join(lines)

    @classmethod
    def format_warning(
        cls,
        filename: Optional[str],
        line_number: Optional[int],
        column: Optional[int],
        message: str,
        source_line: Optional[str] = None,
        hint: Optional[str] = None
    ) -> str:
        """Format a warning message in Clang style."""
        use_color = cls._supports_color()
        lines = []

        location_parts = []
        if filename:
            location_parts.append(f"{filename}")
        if line_number is not None:
            location_parts.append(f"{line_number}")
        if column is not None:
            location_parts.append(f"{column}")

        location = ":".join(location_parts) if location_parts else "stacker"

        if use_color:
            warning_label = f"{cls.BOLD}{cls.YELLOW}warning:{cls.RESET}"
            location = f"{cls.BOLD}{location}{cls.RESET}"
        else:
            warning_label = "warning:"

        lines.append(f"{location}: {warning_label} {message}")

        if source_line is not None and line_number is not None:
            line_num_str = str(line_number)

            if use_color:
                line_prefix = f"{cls.BLUE}{line_num_str} |{cls.RESET} "
                blank_prefix = f"{cls.BLUE}{' ' * len(line_num_str)} |{cls.RESET} "
            else:
                line_prefix = f"{line_num_str} | "
                blank_prefix = f"{' ' * len(line_num_str)} | "

            lines.append(blank_prefix)
            lines.append(f"{line_prefix}{source_line}")

            if column is not None and column > 0:
                indicator_pos = column - 1
                spaces = ' ' * indicator_pos

                if use_color:
                    indicator = f"{blank_prefix}{spaces}{cls.BOLD}{cls.YELLOW}^{cls.RESET}"
                else:
                    indicator = f"{blank_prefix}{spaces}^"

                lines.append(indicator)

        if hint:
            if use_color:
                lines.append(f"{cls.BOLD}{cls.CYAN}hint:{cls.RESET} {hint}")
            else:
                lines.append(f"hint: {hint}")

        return "\n".join(lines)


class StackerErrorWithContext(Exception):
    """
    Enhanced Stacker error with source context information.

    This exception stores additional information needed for
    rich error formatting.
    """

    def __init__(
        self,
        message: str,
        error_type: str = "StackerError",
        filename: Optional[str] = None,
        line_number: Optional[int] = None,
        column: Optional[int] = None,
        source_line: Optional[str] = None,
        hint: Optional[str] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_type = error_type
        self.filename = filename
        self.line_number = line_number
        self.column = column
        self.source_line = source_line
        self.hint = hint

    def format(self) -> str:
        """Format this error using the ErrorFormatter."""
        return ErrorFormatter.format_error(
            filename=self.filename,
            line_number=self.line_number,
            column=self.column,
            error_type=self.error_type,
            message=self.message,
            source_line=self.source_line,
            hint=self.hint
        )

    def __str__(self) -> str:
        """Return formatted error message."""
        return self.format()


--- stacker/stacker/__main__.py ---
import argparse
import importlib
import logging
import os
import shutil
import sys
import traceback
from pathlib import Path
import stacker

from stacker.runtime.exec_modes import CommandLineMode, ReplMode, ScriptMode

from stacker.lib import disp_logo
from stacker.lib.config import plugins_dir_path, stacker_dotfile_path
from stacker.stacker import Stacker
from stacker.util import colored

parser = argparse.ArgumentParser(description="Stacker command line interface.")
parser.add_argument(
    "--addplugin", metavar="path", type=str, help="Path to the plugin to add."
)
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
parser.add_argument("-e", default=None, help="Execute the given command.")
parser.add_argument("script", nargs="?", default=None, help="Script file to run.")
argv = parser.parse_args()

sys.setrecursionlimit(1 << 30)


def load_stacker_lib(stacker: Stacker, dir_path) -> bool:
    """Load the Stacker library from the specified directory.
    :param stacker: The Stacker instance to pass to the plugins.
    :param dir_path: The directory to load the Stacker library from.
    :return: None
    """
    # Add the library directory path
    sys.path.insert(0, dir_path)
    for filename in os.listdir(dir_path):
        try:
            if filename.endswith(".stk"):
                include_stacker_script = Path(dir_path) / filename
                stacker.include(str(include_stacker_script))
        except Exception as e:
            print(colored(f"Failed load slib ({filename}). {e}", "red"))
            sys.path.pop(0)
            return False
    sys.path.pop(0)
    return True


def load_plugins(stacker: Stacker, plugins_dir_path) -> bool:
    """Load plugins from the plugins directory.
    :param stacker: The Stacker instance to pass to the plugins.
    :return: None
    """
    # Add the plugin directory path
    sys.path.insert(0, plugins_dir_path)
    for filename in os.listdir(plugins_dir_path):
        try:
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = os.path.splitext(filename)[0]  # remove .py extension
                plugin_module = importlib.import_module(module_name)
                plugin_module.setup(stacker)
                logging.debug(f"Loaded plugin '{module_name}'.")
        except Exception as e:
            print(colored(f"Failed load plugin ({filename}). {e}", "red"))
            sys.path.pop(0)
            return False
    sys.path.pop(0)
    return True


def load_dotfile(stacker: Stacker, dotfile_path: str | Path) -> None:
    """Load the dotfile.
    :param stacker: The Stacker instance to pass to the plugins.
    :param dotfile_path: The path to the dotfile.
    :return: None
    """
    try:
        if not os.path.isfile(dotfile_path):
            print(f"Error: The file '{dotfile_path}' does not exist.")
            return
        stacker.include(str(dotfile_path))
    except Exception as e:
        print(f"An error occurred while loading the dotfile: {str(e)}")


def copy_plugin_to_install_dir(plugin_path: str, debug_mode: bool) -> None:
    try:
        # Get the installation directory of Stacker
        # stacker_dist = get_distribution("pystacker")
        # plugin_dir = stacker_dist.location + "/stacker/plugins"
        stacker_package_dir = os.path.dirname(os.path.abspath(stacker.__file__))
        plugin_dir = os.path.join(stacker_package_dir, "plugins")

        # Check if the plugin file exists
        if not os.path.isfile(plugin_path):
            print(f"Error: The file '{plugin_path}' does not exist.")
            return

        # Copy the plugin file to the Stacker's installation directory
        assert Path(plugin_dir).exists
        shutil.copy(plugin_path, plugin_dir)
        print(f"Successfully added the plugin '{plugin_path}' to Stacker.")
        print(plugin_dir)
    except Exception as e:
        print(
            f"An error occurred while adding the plugin ({str(plugin_path)}): {str(e)}"
        )
        if debug_mode:
            traceback.print_exc()


def main():
    """Main entry point for the Stacker CLI."""
    # add plugin
    if argv.addplugin:
        copy_plugin_to_install_dir(argv.addplugin, argv.debug)
        return

    if argv.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    rpn_calculator = Stacker()

    # load plugins from the Stacker's installation directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plugins_dir = os.path.join(script_dir, plugins_dir_path)
    if not load_plugins(rpn_calculator, plugins_dir):
        sys.exit(1)

    # load plugins from current directory
    plugins_dir = os.path.join(os.getcwd(), plugins_dir_path)
    if Path(plugins_dir).exists():
        if not load_plugins(rpn_calculator, plugins_dir):
            sys.exit(1)

    # load the Stacker library
    library_dir = os.path.join(script_dir, "slib")
    if not load_stacker_lib(rpn_calculator, library_dir):
        sys.exit(1)

    if argv.e is not None:
        # Execute the given command
        commandline_mode = CommandLineMode(rpn_calculator)
        if stacker_dotfile_path.exists():
            commandline_mode.execute_stacker_dotfile(stacker_dotfile_path)
        commandline_mode.run(argv.e)
        return

    if argv.script:
        # Script Mode
        script_mode = ScriptMode(rpn_calculator)
        if stacker_dotfile_path.exists():
            script_mode.execute_stacker_dotfile(stacker_dotfile_path)
        if argv.debug:
            script_mode.debug_mode()
        rpn_calculator.clear_trace()
        script_mode.run(argv.script)
    else:
        # REPL mode
        repl_mode = ReplMode(rpn_calculator)
        # execute the dotfile
        if stacker_dotfile_path.exists():
            repl_mode.execute_stacker_dotfile(stacker_dotfile_path)
        if argv.debug:
            repl_mode.debug_mode()
        if repl_mode.disp_logo_mode:
            disp_logo()
        rpn_calculator.clear_trace()
        repl_mode.run()


if __name__ == "__main__":
    main()


--- stacker/stacker/error.py ---
from __future__ import annotations

"""
SyntaxError:
This error is thrown during syntax parsing when an unexpected token is found, or an expected token is not found.
Specifically, it occurs when the input expression does not follow the grammar of the language.

UnexpectedTokenError:
A subclass of SyntaxError, this error is thrown during syntax parsing when an unexpected token is encountered.
It is associated with a specific token.

SemanticError:
This error occurs during the evaluation of an expression.
It is thrown when an operation that is syntactically correct but semantically incorrect is performed,
such as referencing an undefined variable.

RuntimeError:
This error is thrown during the execution of the program when a problem occurs in the execution environment.
It includes situations such as memory shortage or failure to access external resources.

ResourceError:
This error is associated with the allocation and release of resources.
It is thrown when necessary resources are not adequately available.

ValidationError:
This error is thrown during the validation of input values when an invalid value is detected.
It applies when the input value is not of the expected type or is outside the allowable range.

LoadPluginError:
This error is thrown when an error occurs while loading a plugin.

UndefinedVariableError:
This error is thrown when an undefined variable is referenced.

------------------------------------------------------------------------------
"""


class StackerError(Exception):
    pass


class StackUnderflowError(StackerError):
    """Stack underflow error"""

    def __init__(self, operator: str, num_args: int):
        message = f"Operator `{operator}` requires {num_args} arguments."
        super().__init__(message)


class StackerSyntaxError(StackerError):
    """Syntax error"""

    def __init__(self, message):
        if message is None:
            message = "An error occurred while parsing the expression."
        super().__init__(message)


class UnexpectedTokenError(StackerError):
    """Unexpected token error"""

    def __init__(self, token, message=None):
        if message is None:
            message = f"`{token}`. If `{token}` is intended as a variable or symbol, ensure it is defined or prepend it with '$'."
        super().__init__(message)


class UndefinedVariableError(StackerError):
    """Undefined variable error"""

    def __init__(self, token, message=None):
        if message is None:
            message = f"`{token}` is not defined."
        super().__init__(message)


class UndefinedSymbolError(StackerError):
    """Undefined symbol error"""

    def __init__(self, token, message=None):
        if message is None:
            message = f"`{token}` is not defined."
        super().__init__(message)


class SemanticError(StackerError):
    """Semantic error"""

    def __init__(self, message=None):
        if message is None:
            message = "An error occurred while evaluating the expression."
        super().__init__(message)


class StackerRuntimeError(StackerError):
    """Runtime error"""

    def __init__(self, message=None):
        if message is None:
            message = "An error occurred during execution."
        super().__init__(message)


class ResourceError(StackerError):
    """Resource error"""

    def __init__(self, message=None):
        if message is None:
            message = "An error occurred while allocating resources."
        super().__init__(message)


class ValidationError(StackerError):
    """Validation error"""

    def __init__(self, message=None):
        if message is None:
            message = "An error occurred while validating the input."
        super().__init__(message)


class LoadPluginError(StackerError):
    """Load plugin error"""

    def __init__(self, message=None):
        if message is None:
            message = "An error occurred while loading the plugin."
        super().__init__(message)


class IncludeError(StackerError):
    """Include error"""

    def __init__(self, message=None):
        if message is None:
            message = "An error occurred while including the file."
        super().__init__(message)


class ScriptReadError(StackerError):
    """Script read error"""

    def __init__(self, message=None):
        if message is None:
            message = "An error occurred while reading the script."
        super().__init__(message)


class DropError(Exception):
    pass


class DupError(Exception):
    pass


class OverError(Exception):
    pass


class SwapError(Exception):
    pass


class RollError(Exception):
    pass


class RotError(Exception):
    pass


class PickError(Exception):
    pass


class NipError(Exception):
    pass


class InsertError(Exception):
    pass


--- stacker/stacker/stacker.py ---
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from stacker.engine.core import StackerCore
from stacker.syntax.parser import parse_expression

if TYPE_CHECKING:
    from stacker.engine.sfunction import StackerFunction

from stacker.engine.data_type import stack_data


class Stacker(StackerCore):
    def __init__(
        self, expression: str | None = None, parent: StackerCore | None = None
    ):
        super().__init__(expression, parent)
        self.trace = []
        self.plugin_descriptions = {}

    def include(self, filename: str) -> None:
        return self.operator_manager.operators["priority"]["include"]["func"](
            self, filename
        )

    def push(self, value: Any) -> None:  # TODO: remove
        self.stack.append(value)

    def pop_and_eval(self, stack: stack_data) -> Any:
        return self._pop_and_eval(stack)

    def pop(self) -> Any:
        return self.stack.pop()

    def process_expression(self, expression) -> None:
        tokens = parse_expression(expression)
        self.evaluate(tokens, stack=self.stack)

    # @staticmethod
    # def new(expression: str | None = None, parent: Stacker | None = None) -> Stacker:
    #     return Stacker(expression=expression, parent=parent)

    def evaluate(self, tokens: list, stack: stack_data = stack_data()) -> stack_data:
        """
        Evaluates a given RPN expression.
        Returns the result of the evaluation.
        """
        try:
            return self._evaluate(tokens, stack=stack)
        except Exception as e:
            if self.parent is not None:
                self.parent.trace = self.trace
            raise e

    def register_operator(
        self,
        operator_name: str,
        operator_func: Callable,
        arg_count: int,
        push_result_to_stack: bool,
        desc: str | None = None,
    ) -> None:
        self.operator_manager.register_operator(
            operator_name,
            operator_func,
            arg_count,
            push_result_to_stack,
            desc,
        )

    def register_sfunction(
        self,
        sfunction_name: str,
        sfunction_func: StackerFunction,
        arg_count: int,
        push_result_to_stack: bool = True,
        desc: str | None = None,
    ) -> None:
        self.sfunctions[sfunction_name] = {
            "func": sfunction_func,
            "arg_count": arg_count,
            "push_result_to_stack": push_result_to_stack,
            "desc": desc,
        }

    def register_macro(self, macro_name: str, macro_body: Callable) -> None:
        self.macros[macro_name] = macro_body

    def register_parameter(self, parameter_name: str, parameter_value: Any) -> None:
        self.variables[parameter_name] = parameter_value

    def register_plugin(
        self,
        operator_name: str,
        operator_func: Any,
        push_result_to_stack: bool = True,
        pass_core: bool = False,
        desc: str | None = None,
    ) -> None:
        if pass_core:
            original_operator_func = operator_func

            def wrapped_operator_func(*args, **kwargs):
                wraped = original_operator_func(self, *args, **kwargs)
                return wraped

            wrapped_operator_func.arg_count = (
                original_operator_func.__code__.co_argcount - 1
            )
            operator_func = wrapped_operator_func
            arg_count = wrapped_operator_func.arg_count
        else:
            arg_count = operator_func.__code__.co_argcount
        # self.register_operator(
        #     operator_name, operator_func, arg_count, push_result_to_stack, desc
        # )
        if operator_name in self.plugins:
            del self.plugins[operator_name]
        self.plugins[operator_name] = {
            "func": operator_func,
            "arg_count": arg_count,
            "push_result_to_stack": push_result_to_stack,
            "desc": desc,
        }
        self.plugin_descriptions[operator_name] = desc

    def register_label(self, label_name: str, index: int) -> None:
        self.labels[label_name] = index

    # ========================
    # Getter
    # ========================

    def get_stack_ref(self) -> stack_data:
        return self.stack

    def get_stack_copy(self) -> stack_data:
        return self.stack.copy()

    def get_stack_copy_as_list(self) -> list:
        return list(self.stack.copy())

    def get_macros_ref(self) -> dict:
        return self.macros

    def get_macros_copy(self) -> dict:
        return self.macros.copy()

    def get_variables_ref(self) -> dict:
        return self.variables

    def get_variables_copy(self) -> dict:
        return self.variables.copy()

    def get_sfuntions_ref(self) -> dict:
        return self.sfunctions

    def get_sfuntions_copy(self) -> dict:
        return self.sfunctions.copy()

    def get_plugins_ref(self) -> dict:
        return self.plugins

    def get_plugins_copy(self) -> dict:
        return self.plugins.copy()

    def get_stack_length(self) -> int:
        return len(self.stack)

    def get_trace_ref(self) -> list[Any]:
        return self.trace

    def get_trace_copy(self) -> list[Any]:
        return self.trace.copy()

    def get_labels_ref(self) -> dict:
        return self.labels

    def get_labels_copy(self) -> dict:
        return self.labels.copy()

    def get_all_keys_for_completer(self) -> list[str]:
        return list(
            set(
                self.operator_manager.get_all_keys_for_completer()
                + list(self.sfunctions.keys())
                + list(self.plugins.keys())
                + list(self.macros.keys())
                + list(self.variables.keys())
            )
        )

    def get_plugin_descriptions(self) -> dict:
        return self.plugin_descriptions

    # ========================
    # Clear
    # ========================

    def clear_trace(self) -> None:
        self.trace = []

    # def clear_ans(self) -> None:
    #     self._ans = None

    # ========================
    # Debug
    # ========================

    def eval(self, expression: str, stack: stack_data = stack_data()) -> Any:
        """Evaluates a given RPN expression.
        Returns the result of the evaluation.

        Example:
        ``` python
        stacker = Stacker()
        and = stacker.eval("1 2 +")
        ```
        """
        tokens = parse_expression(expression)
        return self.evaluate(tokens, stack=stack)


--- stacker/stacker/manager/__init__.py ---
from stacker.operators.manager import OperatorManager

__all__ = ["OperatorManager"]


--- stacker/stacker/lib/ui_tools.py ---
from __future__ import annotations

from importlib.resources import files

from stacker.lib.config import history_file_path
from stacker.util.color import colored


def disp_logo() -> None:
    """Prints the top message."""
    colors = ["red", "green", "yellow", "lightblue", "lightmagenta", "cyan"]
    with files("stacker").joinpath("data/top.txt").open("rb") as f:
        messages = f.readlines()
        for i in range(len(messages)):
            print(colored(messages[i].decode("utf-8"), colors[i]), end="")
    print("")


def disp_about() -> None:
    """Prints the about message."""
    with files("stacker").joinpath("data/about.txt").open("rb") as f:
        message = f.read().decode("utf-8")
    print(message)


def disp_help() -> None:
    """Prints the help message."""
    with files("stacker").joinpath("data/help.txt").open("rb") as f:
        message = f.read().decode("utf-8")
    print(message)


def delete_history() -> None:
    """Deletes the history file."""
    if history_file_path.exists():
        history_file_path.unlink()


--- stacker/stacker/lib/__init__.py ---
from stacker.lib.ui_tools import delete_history, disp_about, disp_help, disp_logo

__all__ = [
    "disp_logo",
    "disp_about",
    "disp_help",
    "delete_history",
]


--- stacker/stacker/lib/config.py ---
from __future__ import annotations

from pathlib import Path

history_file = ".stacker_history"
history_file_path = Path.home() / history_file
plugins_dir_path = "plugins"

stacker_dotfile = ".stackerrc"
stacker_dotfile_path = Path.home() / stacker_dotfile

script_extension_name = ".stk"


--- stacker/stacker/slib/__init__.py ---


--- stacker/stacker/slib/macro.stk ---


--- stacker/stacker/slib/sfunction.stk ---

"""
mean: Mean of a list of numbers
"""
{xs} {xs sum xs len /} $mean defun


--- stacker/stacker/data/help.txt ---
Enter RPN expression, variable assignment, or function definition.
Type 'exit' to quit.

Usage:
  Input numbers and operators in RPN notation, separated by spaces.
  Press Enter to evaluate the expression and display the result.
  The result will be pushed onto the stack.
  To use the result in a subsequent calculation, input the next expression.
  To clear the stack, type 'clear'.

Numbwer input:
  integer: 3
  float: 3.14
  scientific notation: 1.23e-4
  hexadecimal: 0x1a
  binary: 0b1010
  octal: 0o123
  complex: 1+2j

String input:
  "hogefoovar"

Array input:
  [1 2 3 4 5]
  [1 2 3; 4 5 6; 7 8 9]
Tuple input:
  (1 2 3 4 5)
  (1 2 3; 4 5 6; 7 8 9)

If statement:
  condition <true expr> if
  condition <true expr> <false expr> ifelse

Loop statement:
  - do
    stat end $loopVariable {body} do
  - times
    {body} n times

Define Function:
  {arg1 srg2 ...} {body} $funcName defun

Lambda:
  {arg1 srg2 ...} {body} lambda

Macro:
  {body} $macroName defmacro

parameters:
  pi
  e
  inf
  nan
  true
  false
  null

--- stacker/stacker/data/top.txt ---
  _____  _                 _
 / ____|| |               | |
| (___  | |_   __ _   ___ | | __  ___  _ __
 \___ \ | __| / _` | / __|| |/ / / _ \| '__|
 ____) || |_ | (_| || (__ |   < |  __/| |
|_____/  \__| \__,_| \___||_|\_\ \___||_|


--- stacker/stacker/data/about.txt ---
Welcome to Stacker, where we stack things up - but only in the right order! 😉
This powerful, yet humble, Reverse Polish Notation (RPN) calculator is here to make your life easier.
We know, it's not every day you encounter a calculator that loves postfix expressions as much as we do. 🤓

With Stacker, you'll experience the joy of crunching numbers without the hassle of parentheses. 🥴
Our calculator is so dedicated to the cause that it even lets you define your own functions - isn't that fantastic? 🚀

So, go ahead and give Stacker a spin! Just remember, if you ever feel lost, type "help" and we'll be there for you.
Happy stacking! 🎉

--- stacker/stacker/operators/os.py ---
from __future__ import annotations

from pathlib import Path
import os


def _ls() -> list[str]:
    return [p.name for p in Path(".").iterdir()]


def _cd(path: str) -> None:
    os.chdir(path)


def _pwd() -> str:
    return os.getcwd()


def _cat(filename: str) -> str:
    with open(filename, "r") as f:
        print(f.read())


os_operators = {
    "ls": {
        "func": lambda: _ls(),
        "arg_count": 0,
        "push_result_to_stack": True,
        "desc": "List files in the current directory",
    },
    "cd": {
        "func": lambda path: _cd(path),
        "arg_count": 1,
        "push_result_to_stack": False,
        "desc": "Change directory to the specified path",
    },
    "pwd": {
        "func": lambda: _pwd(),
        "arg_count": 0,
        "push_result_to_stack": True,
        "desc": "Print the current working directory",
    },
    "cat": {
        "func": lambda filename: _cat(filename),
        "arg_count": 1,
        "push_result_to_stack": False,
        "desc": "Print the contents of a file",
    },
}


--- stacker/stacker/operators/comparison.py ---
from __future__ import annotations


compare_operators = {
    "==": {
        "func": (lambda x1, x2: x1 == x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Equal",
    },
    "!=": {
        "func": (lambda x1, x2: x1 != x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Not equal",
    },
    "<=": {
        "func": (lambda x1, x2: x1 <= x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Less than or equal to",
    },
    "<": {
        "func": (lambda x1, x2: x1 < x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Less than",
    },
    ">=": {
        "func": (lambda x1, x2: x1 >= x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Greater than or equal to",
    },
    ">": {
        "func": (lambda x1, x2: x1 > x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Greater than",
    },
    "eq": {
        "func": (lambda x1, x2: x1 == x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Equal",
    },
    "neq": {
        "func": (lambda x1, x2: x1 != x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Not equal",
    },
    "le": {
        "func": (lambda x1, x2: x1 <= x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Less than or equal to",
    },
    "lt": {
        "func": (lambda x1, x2: x1 < x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Less than",
    },
    "ge": {
        "func": (lambda x1, x2: x1 >= x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Greater than or equal to",
    },
    "gt": {
        "func": (lambda x1, x2: x1 > x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Greater than",
    },
}


--- stacker/stacker/operators/include.py ---
from __future__ import annotations
from stacker.include import include_stacker_script

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stacker.stacker import Stacker


def include(stacker: Stacker, filename: str) -> None:
    """Includes another stacker script."""
    _stacker = include_stacker_script(filename)
    _macros = _stacker.get_macros_ref()
    _variables = _stacker.get_variables_copy()
    _sfunctions = _stacker.get_sfuntions_ref()
    stacker.macros.update(_macros)
    stacker.variables.update(_variables)
    stacker.sfunctions.update(_sfunctions)


include_operators = {
    "include": {
        "func": (lambda stacker, filename: include(stacker, filename)),
        "arg_count": 1,
        "push_result_to_stack": False,
        "desc": "Includes another stacker script.",
    },
}


--- stacker/stacker/operators/bitwise.py ---
from __future__ import annotations


bitwise_operators = {
    "band": {
        "func": (lambda x1, x2: x1 & x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Bitwise and",
    },
    "bor": {
        "func": (lambda x1, x2: x1 | x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Bitwise or",
    },
    "bxor": {
        "func": (lambda x1, x2: x1 ^ x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Bitwise xor",
    },
    "~": {
        "func": (lambda x: ~x),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Bitwise invert",
    },
    ">>": {
        "func": (lambda value, n: value >> n),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Bitwise right shift",
    },
    "<<": {
        "func": (lambda value, n: value << n),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Bitwise left shift",
    },
}


--- stacker/stacker/operators/loop.py ---
from __future__ import annotations

from typing import TYPE_CHECKING, Any
from stacker.reserved import __BREAK__

if TYPE_CHECKING:
    from stacker.stacker import Stacker


def _update_nested_variables(tokens, new_variables):
    """Recursively update variable references in nested StackerCore instances."""
    from stacker.engine.core import StackerCore
    for token in tokens:
        if isinstance(token, StackerCore):
            token.variables = new_variables
            # Recursively update nested code blocks
            _update_nested_variables(token.tokens, new_variables)


def _times(
    n_times: int,
    block: Stacker | Any,
    parent: Stacker,
):
    """Executes a block of code a specified number of times."""
    i_count = 0
    parent.stack.append(i_count)
    while parent.stack[-1] < n_times:
        parent.stack.pop()
        if isinstance(block, type(parent)):
            parent.evaluate(block.tokens, stack=parent.stack)
        else:
            parent.stack.append(block)
        i_count = i_count + 1
        parent.stack.append(i_count)
    parent.stack.pop()


def _do(
    start_value: int,
    end_value: int,
    symbol: str,
    block: Stacker,
    parent: Stacker,
):
    # Create child scope once for all iterations (optimization)
    original_parent_vars = parent.variables
    child_scope = parent.variables.create_child_scope()

    # Update nested StackerCore instances to use the child scope
    _update_nested_variables(block.tokens, child_scope)

    for i in range(start_value, end_value + 1):
        # Update loop variable
        child_scope[symbol] = i
        parent.variables = child_scope
        # Use parent.evaluate to ensure proper context
        parent.evaluate(block.tokens, stack=parent.stack)
        if len(parent.stack) > 0 and parent.stack[-1] == __BREAK__:
            parent.stack.pop()
            break

    parent.variables = original_parent_vars


def _dolist(
    symbol: str,
    lst: list,
    block: Stacker,
    parent: Stacker,
):
    # Create child scope once for all iterations (optimization)
    original_parent_vars = parent.variables
    child_scope = parent.variables.create_child_scope()

    # Update nested StackerCore instances to use the child scope
    # This is necessary because block.tokens may contain nested code blocks
    _update_nested_variables(block.tokens, child_scope)

    for i in lst:
        # Update loop variable
        child_scope[symbol] = i
        parent.variables = child_scope
        # Use parent.evaluate to ensure proper context
        parent.evaluate(block.tokens, stack=parent.stack)
        if len(parent.stack) > 0 and parent.stack[-1] == __BREAK__:
            parent.stack.pop()
            break

    parent.variables = original_parent_vars


loop_operators = {
    "times": {
        "func": (lambda n_times, block, parent: _times(n_times, block, parent)),
        "arg_count": 2,
        "push_result_to_stack": False,
        "desc": "Executes a block of code a specified number of times.",
    },
    "do": {
        "func": (
            lambda start_value, end_value, symbol, block, parent: _do(
                start_value, end_value, symbol, block, parent
            )
        ),
        "arg_count": 4,
        "push_result_to_stack": False,
        "desc": "Executes a block of code a specified number of times.",
    },
    "dolist": {
        "func": (
            lambda symbol, lst, block, parent: _dolist(symbol, lst, block, parent)
        ),
        "arg_count": 4,
        "push_result_to_stack": False,
        "desc": "Executes a block of code a specified number of times.",
    },
}


--- stacker/stacker/operators/random.py ---
from __future__ import annotations

import random


def _rand() -> float:
    return random.random()


def _randint(x1: int, x2: int) -> int:
    return random.randint(int(x1), int(x2))


def _uniform(x1: float, x2: float) -> float:
    return random.uniform(float(x1), float(x2))


def _dice(num_dice: int, num_faces: int) -> int:
    # Roll dice (e.g., 3d6)
    return sum(random.randint(1, int(num_faces)) for _ in range(int(num_dice)))


random_operators = {
    "rand": {
        "func": (lambda: _rand()),
        "arg_count": 0,
        "push_result_to_stack": True,
        "desc": "Generate random float between 0 and 1",
    },
    "randint": {
        "func": (lambda x1, x2: _randint(x1, x2)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Generate random int between x1 and x2",
    },
    "uniform": {
        "func": (lambda x1, x2: _uniform(x1, x2)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Generate random float between x1 and x2",
    },
    "dice": {
        "func": (lambda num_dice, num_faces: _dice(num_dice, num_faces)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Roll D&D-style dice (e.g., 3d6 = 3 6 dice)",
    },
}


--- stacker/stacker/operators/logic.py ---
from __future__ import annotations


# def xor(x1, x2):
#     try:
#         return (x1 ^ x2)
#     except TypeError:
#         raise TypeError("Cannot Logical xor {} and {}".format(type(x1), type(x2)))


logic_operators = {
    "and": {
        "func": (lambda x1, x2: x1 and x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Logical and",
    },
    "or": {
        "func": (lambda x1, x2: x1 or x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Logical or",
    },
    "not": {
        "func": (lambda x: not x),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Logical not",
    },
    "&&": {
        "func": (lambda x1, x2: x1 and x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Logical and",
    },
    "||": {
        "func": (lambda x1, x2: x1 or x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Logical or",
    },
}


--- stacker/stacker/operators/if_else.py ---
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from stacker.stacker import Stacker


def _if(condition: Stacker | bool, blockstack: Stacker | Any, parent: Stacker) -> None:
    """Executes a block of code if a condition is true.
    {block}
    {condition}
    if
    """
    if isinstance(condition, type(parent)):
        parent.evaluate(condition.tokens, stack=parent.stack)
        condition = parent.stack.pop()
    if isinstance(condition, str):
        if condition in parent.variables:
            condition = parent.variables[condition]
    if condition:
        if isinstance(blockstack, type(parent)):
            parent.evaluate(blockstack.tokens, stack=parent.stack)
        else:  # e.g. a numeric object
            parent.stack.append(blockstack)


def _if_else(
    condition: Stacker | bool,
    true_block: Stacker | Any,
    false_block: Stacker | Any,
    parent: Stacker,
) -> None:
    """Executes a block of code if a condition is true, otherwise executes another block of code.
    {true block}
    {false block}
    {condition}
    ifelse
    """
    if isinstance(condition, type(parent)):
        parent.evaluate(condition.tokens, stack=parent.stack)
        condition = parent.stack.pop()
    if isinstance(condition, str):
        if condition in parent.variables:
            condition = parent.variables[condition]
    if condition:
        if isinstance(true_block, type(parent)):
            parent.evaluate(true_block.tokens, stack=parent.stack)
        else:  # e.g. a numeric object
            parent.stack.append(true_block)
    else:
        if isinstance(false_block, type(parent)):
            parent.evaluate(false_block.tokens, stack=parent.stack)
        else:
            parent.stack.append(false_block)


def _iferror(
    try_block: Stacker | Any,
    catch_block: Stacker | Any,
    parent: Stacker,
):
    """Executes a block of code if an error occurs.
    {try block}
    {catch block}
    iferror
    """
    try:
        if isinstance(try_block, type(parent)):
            parent.evaluate(try_block.tokens, stack=parent.stack)
        else:
            parent.stack.append(try_block)
    except Exception as _:
        if isinstance(catch_block, type(parent)):
            parent.evaluate(catch_block.tokens, stack=parent.stack)
        else:
            parent.stack.append(catch_block)


condition_operators = {
    "if": {
        "func": (
            lambda condition, blockstack, parent: _if(condition, blockstack, parent)
        ),
        "arg_count": 2,
        "push_result_to_stack": False,
        "desc": "Executes a block of code if a condition is true.",
    },
    "ifelse": {
        "func": (
            lambda condition, true_block, false_block, parent: _if_else(
                condition, true_block, false_block, parent
            )
        ),
        "arg_count": 3,
        "push_result_to_stack": False,
        "desc": (
            "Executes a block of code if a condition is true, "
            "otherwise executes another block of code."
        ),
    },
    "iferror": {
        "func": (
            lambda try_block, catch_block, parent: _iferror(
                try_block, catch_block, parent
            )
        ),
        "arg_count": 2,
        "push_result_to_stack": False,
        "desc": "Executes a block of code if an error occurs.",
    },
}


--- stacker/stacker/operators/io.py ---
from __future__ import annotations

io_operators = {
    "echo": {
        "func": (lambda content: print(content)),
        "arg_count": 1,
        "push_result_to_stack": False,
        "desc": "Prints the specified content to the console.",
    },
    "print": {
        "func": (lambda content: print(content)),
        "arg_count": 1,
        "push_result_to_stack": False,
        "desc": "Prints the specified content to the console.",
    },
    "printc": {
        "func": (lambda content: print(content, end="")),
        "arg_count": 1,
        "push_result_to_stack": False,
        "desc": "Prints the specified content to the console without a newline.",
    },
    "newline": {
        "func": (lambda: print("")),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Prints a newline to the console.",
    },
    # "input": {
    #     "func": (lambda: _input()),
    #     "arg_count": 0,
    #     "push_result_to_stack": True,
    #     "desc": "Reads a line of input from the console.",
    # },
}


--- stacker/stacker/operators/defun.py ---
from __future__ import annotations

from typing import TYPE_CHECKING
from stacker.engine.sfunction import StackerFunction


if TYPE_CHECKING:
    from stacker.stacker import Stacker


def defun_sfunction(
    stacker: Stacker, func_name: str, fargs: list, body: Stacker
) -> None:
    function = StackerFunction(fargs, body)
    args_count = len(fargs)
    stacker.register_sfunction(
        func_name, function, args_count, push_result_to_stack=True
    )


defun_operators = {
    "defun": {
        "func": (
            lambda stacker, func_name, fargs, body: defun_sfunction(
                stacker, func_name, fargs, body
            )
        ),
        "arg_count": 3,
        "push_result_to_stack": False,
        "desc": "Defines a function.",
    },
}


--- stacker/stacker/operators/time.py ---
from __future__ import annotations

from time import time


def _time() -> float:
    """Returns the current time in seconds since the Epoch."""
    return time()


time_operators = {
    "time": {
        "func": (lambda: _time()),
        "arg_count": 0,
        "push_result_to_stack": True,
        "desc": "Returns the current time in seconds since the Epoch.",
    },
}


--- stacker/stacker/operators/algebra.py ---
from __future__ import annotations


alge_operators = {
    "neg": {
        "func": (lambda x: -x),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Negate",
    },
}


--- stacker/stacker/operators/__init__.py ---


--- stacker/stacker/operators/eval.py ---
from __future__ import annotations

from stacker.error import StackerSyntaxError

# def _stacker_eval(expr: str, stacker: "Stacker"):
#     """Evaluates a given RPN expression.
#     Returns the result of the evaluation.
#     """
#     if not isinstance(expr, str):
#         raise StackerSyntaxError("Invalid expression")
#     if (expr.startswith("'") and expr.endswith("'")) or (
#         expr.startswith('"') and expr.endswith('"')
#     ):
#         return eval(expr[1:-1])
#     else:
#         raise StackerSyntaxError("Invalid expression. Only string is allowed.")


eval_operators = {
    # "eval": {
    # },
}


--- stacker/stacker/operators/arith.py ---
from __future__ import annotations


arith_operators = {
    "+": {
        "func": (lambda x1, x2: x1 + x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Add",
    },
    "-": {
        "func": (lambda x1, x2: x1 - x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Subtract",
    },
    "*": {
        "func": (lambda x1, x2: x1 * x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Multiply",
    },
    "//": {
        "func": (lambda x1, x2: x1 // x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Integer divide",
    },
    "/": {
        "func": (lambda x1, x2: x1 / x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Divide",
    },
    "%": {
        "func": (lambda x1, x2: x1 % x2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Mod",
    },
    "++": {
        "func": (lambda x: x + 1),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Increment",
    },
    "--": {
        "func": (lambda x: x - 1),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Decrement",
    },
}


--- stacker/stacker/operators/aggregate.py ---
from __future__ import annotations


aggregate_operators = {
    "any": {
        "func": (lambda xs: any(xs)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Returns True if any element of an iterable is True.",
    },
    "all": {
        "func": (lambda xs: all(xs)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Returns True if all elements of an iterable are True.",
    },
    "sum": {
        "func": (lambda xs: sum(xs)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Sums a iterable.",
    },
    "len": {
        "func": (lambda xs: len(xs)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Returns the length of an iterable.",
    },
    "min": {
        "func": (lambda xs: min(xs)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Returns the minimum value in an iterable.",
    },
    "max": {
        "func": (lambda xs: max(xs)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Returns the maximum value in an iterable.",
    },
}


--- stacker/stacker/operators/list.py ---
from __future__ import annotations


list_operators = {
    "seq": {
        "func": (lambda x1, x2: list(range(x1, x2 + 1))),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Generate sequence from x1 to x2",
    },
    # "range": {
    #     "func": (lambda x1, x2: range(x1, x2)),
    #     "arg_count": 2,
    #     "push_result_to_stack": True,
    #     "desc": "Generate range from x1 to x2",
    # },
    # "append": {
    #     "func": (lambda xs, x: xs.append(x)),
    #     "arg_count": 2,
    #     "push_result_to_stack": True,
    #     "desc": "Append value to list",
    # },
    # "extend": {
    #     "func": (lambda xs1, xs2: xs1.extend(xs2)),
    #     "arg_count": 2,
    #     "push_result_to_stack": True,
    #     "desc": "Extend list",
    # },
    # "insert": {
    #     "func": (lambda xs, i, x: xs.insert(i, x)),
    #     "arg_count": 3,
    #     "push_result_to_stack": True,
    #     "desc": "Insert value into list",
    # },
    # "reverse": {
    #     "func": (lambda xs: xs.reverse()),
    #     "arg_count": 1,
    #     "push_result_to_stack": True,
    #     "desc": "Reverse list",
    # },
    # "sort": {
    #     "func": (lambda xs: xs.sort()),
    #     "arg_count": 1,
    #     "push_result_to_stack": True,
    #     "desc": "Sort list",
    # },
    # "count": {
    #     "func": (lambda xs, x: xs.count(x)),
    #     "arg_count": 2,
    #     "push_result_to_stack": True,
    #     "desc": "Count value in list",
    # },
}


--- stacker/stacker/operators/manager.py ---
from __future__ import annotations

from typing import Callable

from stacker.error import StackerSyntaxError


from stacker.operators.algebra import alge_operators
from stacker.operators.arith import arith_operators
from stacker.operators.aggregate import aggregate_operators
from stacker.operators.transform import transform_operators
from stacker.operators.base import base_operators
from stacker.operators.bitwise import bitwise_operators
from stacker.operators.comparison import compare_operators
from stacker.operators.eval import eval_operators
from stacker.operators.file import file_operators
from stacker.operators.io import io_operators
from stacker.operators.list import list_operators
from stacker.operators.logic import logic_operators
from stacker.operators.math import math_operators
from stacker.operators.random import random_operators
from stacker.operators.stack import stack_operators
from stacker.operators.string import string_operators
from stacker.operators.time import time_operators
from stacker.operators.types import type_operators
from stacker.operators.loop import loop_operators
from stacker.operators.if_else import condition_operators
from stacker.operators.include import include_operators
from stacker.operators.setting import settings_operators
from stacker.operators.exit import exit_operators
from stacker.operators.defun import defun_operators
from stacker.operators.defmacro import macro_operators
from stacker.operators.hof import hof_operators
from stacker.operators.lmd import lambda_operators
from stacker.operators.os import os_operators
from stacker.operators.system import system_operators


special_operators = {
    "ans": {
        "func": None,
        "arg_count": 0,
        "push_result_to_stack": True,
        "desc": "Returns the last result.",
    },
    "set": {
        "func": None,
        "arg_count": 2,
        "push_result_to_stack": False,
        "desc": "Sets a variable (updates existing or creates local).",
    },
    "=": {
        "func": None,
        "arg_count": 2,
        "push_result_to_stack": False,
        "desc": "Sets a variable (updates existing or creates local).",
    },
    "global": {
        "func": None,
        "arg_count": 2,
        "push_result_to_stack": False,
        "desc": "Sets a variable in global scope.",
    },
    "eval": {
        "func": None,
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Evaluates a given RPN expression.",
    },
    "break": {
        "func": None,
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Breaks a loop.",
    },
    "sub": {
        "func": None,
        "arg_count": 0,
        "push_result_to_stack": True,
        "desc": "Substack the top element",
    },
    "subn": {
        "func": None,
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Cluster elements between the top and the nth (make substacks)",
    },
    "read-from-string": {
        "func": None,
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Reads a string and returns a list of words.",
    },
    "read": {
        "func": None,
        "arg_count": 0,
        "push_result_to_stack": True,
        "desc": "Reads a string from the console.",
    },
    "split": {
        "func": None,
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Splits the first string by the second string.",
    },
    "nth": {
        "func": None,
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Returns the nth element of the iterable.",
    },
    "expand": {
        "func": None,
        "arg_count": 1,
        "push_result_to_stack": False,
        "desc": "Unlists a iterable.",
    },
    "listn": {
        "func": None,
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Converts an iterable to a list.",
    },
    # REMOVED: "tuplen" operator - () now creates code blocks, not tuples
    # Use lists [] instead of tuples for data structures
}


class OperatorManager:
    def __init__(self):
        self._regular_operators = {}
        self._regular_operators.update(alge_operators)
        self._regular_operators.update(arith_operators)
        self._regular_operators.update(base_operators)
        self._regular_operators.update(bitwise_operators)
        self._regular_operators.update(compare_operators)
        self._regular_operators.update(file_operators)
        self._regular_operators.update(io_operators)
        self._regular_operators.update(logic_operators)
        self._regular_operators.update(math_operators)
        self._regular_operators.update(random_operators)
        self._regular_operators.update(type_operators)
        self._regular_operators.update(list_operators)
        self._regular_operators.update(eval_operators)
        self._regular_operators.update(string_operators)
        self._regular_operators.update(time_operators)
        self._regular_operators.update(os_operators)

        self._priority_operators = {}
        self._priority_operators.update(loop_operators)
        self._priority_operators.update(condition_operators)
        self._priority_operators.update(special_operators)
        self._priority_operators.update(include_operators)
        self._priority_operators.update(defun_operators)
        self._priority_operators.update(macro_operators)
        self._priority_operators.update(lambda_operators)
        self._priority_operators.update(exit_operators)

        self._file_operators = file_operators
        self._hof_operators = hof_operators
        self._aggregate_operators = aggregate_operators
        self._transform_operators = transform_operators
        self._stack_operators = stack_operators
        self._settings_operators = settings_operators
        self._system_operators = system_operators

        self.operators = {
            "priority": self._priority_operators,
            "regular": self._regular_operators,
            "hof": self._hof_operators,
            "aggregate": self._aggregate_operators,
            "transform": self._transform_operators,
            "stack": self._stack_operators,
            "file": self._file_operators,
            "settings": self._settings_operators,
            "system": self._system_operators,
        }

        self.built_in_operators = set()
        for kind in self.operators.keys():
            self.built_in_operators.update(self.operators[kind].keys())

    def get_all_keys_for_completer(self) -> list[str]:
        return list(
            set(
                self.get_regular_keys()
                + self.get_priority_keys()
                + self.get_hof_keys()
                + self.get_aggregate_keys()
                + self.get_transform_keys()
                + self.get_stack_keys()
                + self.get_system_keys()
                # + list(self.get_settings_keys())
            )
        )

    def get_any_operator_arg_count(self, operator: str) -> int:
        if operator in self._priority_operators:
            return self._priority_operators[operator]["arg_count"]
        if operator in self._regular_operators:
            return self._regular_operators[operator]["arg_count"]
        if operator in special_operators:
            return special_operators[operator]["arg_count"]
        if operator in hof_operators:
            return hof_operators[operator]["arg_count"]
        if operator in aggregate_operators:
            return aggregate_operators[operator]["arg_count"]
        if operator in transform_operators:
            return transform_operators[operator]["arg_count"]
        if operator in stack_operators:
            return stack_operators[operator]["arg_count"]
        if operator in file_operators:
            return file_operators[operator]["arg_count"]
        if operator in settings_operators:
            return settings_operators[operator]["arg_count"]
        if operator in system_operators:
            return system_operators[operator]["arg_count"]
        raise StackerSyntaxError(f"Unknown operator '{operator}'")

    ############################
    # Regular operators
    ############################
    def get_regular_ref(self) -> dict:
        return self._regular_operators

    def get_regular_copy(self) -> dict:
        return self._regular_operators.copy()

    def get_regular_keys(self) -> list[str]:
        return list(self._regular_operators.keys())

    ############################
    # Priority operators
    ############################
    def get_priority_ref(self) -> dict:
        return self._priority_operators

    def get_priority_copy(self) -> dict:
        return self._priority_operators.copy()

    def get_priority_keys(self) -> list[str]:
        return list(self._priority_operators.keys())

    ############################
    # Special operators
    ############################
    def get_special_ref(self) -> dict:
        return special_operators

    def get_special_copy(self) -> dict:
        return special_operators.copy()

    def get_special_keys(self) -> list[str]:
        return list(special_operators.keys())

    ############################
    # HOF operators
    ############################
    def get_hof_ref(self) -> dict:
        return self._hof_operators

    def get_hof_copy(self) -> dict:
        return self._hof_operators.copy()

    def get_hof_keys(self) -> list[str]:
        return list(self._hof_operators.keys())

    ############################
    # Aggregate operators
    ############################
    def get_aggregate_ref(self) -> dict:
        return self._aggregate_operators

    def get_aggregate_copy(self) -> dict:
        return self._aggregate_operators.copy()

    def get_aggregate_keys(self) -> list[str]:
        return list(self._aggregate_operators.keys())

    ############################
    # Transform operators
    ############################
    def get_transform_ref(self) -> dict:
        return self._transform_operators

    def get_transform_copy(self) -> dict:
        return self._transform_operators.copy()

    def get_transform_keys(self) -> list[str]:
        return list(self._transform_operators.keys())

    ############################
    # Stack operators
    ############################
    def get_stack_ref(self) -> dict:
        return self._stack_operators

    def get_stack_copy(self) -> dict:
        return self._stack_operators.copy()

    def get_stack_keys(self) -> list[str]:
        return list(self._stack_operators.keys())

    ############################
    # File operators
    ############################
    def get_file_ref(self) -> dict:
        return self._file_operators

    def get_file_copy(self) -> dict:
        return self._file_operators.copy()

    def get_file_keys(self) -> list[str]:
        return list(self._file_operators.keys())

    ############################
    # Settings operators
    ############################
    def get_settings_ref(self) -> dict:
        return self._settings_operators

    def get_settings_copy(self) -> dict:
        return self._settings_operators.copy()

    def get_settings_keys(self) -> list[str]:
        return list(self._settings_operators.keys())

    ############################
    # System operators
    ############################
    def get_system_ref(self) -> dict:
        return self._system_operators

    def get_system_copy(self) -> dict:
        return self._system_operators.copy()

    def get_system_keys(self) -> list[str]:
        return list(self._system_operators.keys())

    ############################
    # Descriptions
    ############################
    def get_priority_descriptions(self) -> dict:
        descriptions = {}
        for operator in self._priority_operators:
            descriptions[operator] = self._priority_operators[operator]["desc"]
        return descriptions

    def get_hof_descriptions(self) -> dict:
        descriptions = {}
        for operator in self._hof_operators:
            descriptions[operator] = self._hof_operators[operator]["desc"]
        return descriptions

    def get_aggregate_descriptions(self) -> dict:
        descriptions = {}
        for operator in self._aggregate_operators:
            descriptions[operator] = self._aggregate_operators[operator]["desc"]
        return descriptions

    def get_transform_descriptions(self) -> dict:
        descriptions = {}
        for operator in self._transform_operators:
            descriptions[operator] = self._transform_operators[operator]["desc"]
        return descriptions

    def get_stack_descriptions(self) -> dict:
        descriptions = {}
        for operator in self._stack_operators:
            descriptions[operator] = self._stack_operators[operator]["desc"]
        return descriptions

    def get_file_descriptions(self) -> dict:
        descriptions = {}
        for operator in self._file_operators:
            descriptions[operator] = self._file_operators[operator]["desc"]
        return descriptions

    def get_settings_descriptions(self) -> dict:
        descriptions = {}
        for operator in self._settings_operators:
            descriptions[operator] = self._settings_operators[operator]["desc"]
        return descriptions

    def get_system_descriptions(self) -> dict:
        descriptions = {}
        for operator in self._system_operators:
            descriptions[operator] = self._system_operators[operator]["desc"]
        return descriptions

    def get_regular_descriptions(self) -> dict:
        descriptions = {}
        for operator in self._regular_operators:
            descriptions[operator] = self._regular_operators[operator]["desc"]
        return descriptions

    def get_regular_and_priority_operator_descriptions(self) -> dict:
        descriptions = {}
        descriptions.update(self.get_regular_descriptions())
        descriptions.update(self.get_priority_descriptions())
        return descriptions

    ############################
    # Register
    ############################
    def register_operator(
        self,
        operator_name: str,
        operator_func: Callable,
        arg_count: int,
        push_result_to_stack: bool,
        desc: str | None = None,
    ) -> None:
        for item in self.operators:
            if operator_name in self.operators[item]:
                del self.operators[item][operator_name]
                self.operators[item][operator_name] = {
                    "func": operator_func,
                    "arg_count": arg_count,
                    "push_result_to_stack": push_result_to_stack,
                    "desc": desc,
                }
                return
        return


--- stacker/stacker/operators/math.py ---
from __future__ import annotations

import math
import cmath
from typing import Callable
from fractions import Fraction


def _pow(x1, x2):
    return x1**x2


def _log(x):
    if type(x) is complex:
        return cmath.log(x)
    else:
        return math.log(x)


def _log2(x):
    if type(x) is complex:
        return cmath.log(x, 2)
    else:
        return math.log(x, 2)


def _log10(x):
    if type(x) is complex:
        return cmath.log(x, 10)
    else:
        return math.log10(x)


def _exp(x):
    if type(x) is complex:
        return cmath.exp(x)
    else:
        return math.exp(x)


def _sin(x):
    if type(x) is complex:
        return cmath.sin(x)
    else:
        return math.sin(x)


def _cos(x):
    if type(x) is complex:
        return cmath.cos(x)
    else:
        return math.cos(x)


def _tan(x):
    if type(x) is complex:
        return cmath.tan(x)
    else:
        return math.tan(x)


def _asin(x):
    if type(x) is complex:
        return cmath.asin(x)
    else:
        return math.asin(x)


def _acos(x):
    if type(x) is complex:
        return cmath.acos(x)
    else:
        return math.acos(x)


def _atan(x):
    if type(x) is complex:
        return cmath.atan(x)
    else:
        return math.atan(x)


def _sinh(x):
    if type(x) is complex:
        return cmath.sinh(x)
    else:
        return math.sinh(x)


def _cosh(x):
    if type(x) is complex:
        return cmath.cosh(x)
    else:
        return math.cosh(x)


def _tanh(x):
    if type(x) is complex:
        return cmath.tanh(x)
    else:
        return math.tanh(x)


def _asinh(x):
    if type(x) is complex:
        return cmath.asinh(x)
    else:
        return math.asinh(x)


def _acosh(x):
    if type(x) is complex:
        return cmath.acosh(x)
    else:
        return math.acosh(x)


def _atanh(x):
    if type(x) is complex:
        return cmath.atanh(x)
    else:
        return math.atanh(x)


def _sqrt(x):
    if type(x) is complex:
        return cmath.sqrt(x)
    else:
        return math.sqrt(x)


def _gcd(x1, x2):
    return math.gcd(x1, x2)


def _lcm(x1, x2):
    return (x1 * x2) // math.gcd(x1, x2)


def _radians(deg):
    return math.radians(deg)


def _factorial(x):
    return math.factorial(x)


def _ceil(x):
    return math.ceil(x)


def _floor(x):
    return math.floor(x)


def _roundn(x, n):
    return round(x, n)


def _round(x):
    return round(x)


def _comb(n: int, k: int):
    return math.comb(int(n), int(k))


def _perm(n: int, k: int) -> int:
    return math.perm(int(n), int(k))


def _abs(x):
    return abs(x)


def _cbrt(x):
    return x ** (1 / 3)


def _ncr(n, k):
    return _comb(n, k)


def _npr(n, k):
    return _perm(n, k)


def _frac(a, b):
    return Fraction(a, b)


def _numeric_diff(f: Callable, x: float) -> float:
    h = 1e-4
    return (f(x + h) - f(x - h)) / (2 * h)


math_operators = {
    "^": {
        "func": (lambda x1, x2: _pow(x1, x2)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Power",
    },
    "log": {
        "func": (lambda x: _log(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Logarithm",
    },
    "log2": {
        "func": (lambda x: _log2(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Logarithm base 2",
    },
    "log10": {
        "func": (lambda x: _log10(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Logarithm base 10",
    },
    "exp": {
        "func": (lambda x: _exp(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Exponential",
    },
    "sin": {
        "func": (lambda x: _sin(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Sine",
    },
    "cos": {
        "func": (lambda x: _cos(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Cosine",
    },
    "tan": {
        "func": (lambda x: _tan(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Tangent",
    },
    "asin": {
        "func": (lambda x: _asin(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Arcsine",
    },
    "acos": {
        "func": (lambda x: _acos(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Arccosine",
    },
    "atan": {
        "func": (lambda x: _atan(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Arctangent",
    },
    "sinh": {
        "func": (lambda x: _sinh(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Hyperbolic sine",
    },
    "cosh": {
        "func": (lambda x: _cosh(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Hyperbolic cosine",
    },
    "tanh": {
        "func": (lambda x: _tanh(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Hyperbolic tangent",
    },
    "asinh": {
        "func": (lambda x: _asinh(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Hyperbolic arcsine",
    },
    "acosh": {
        "func": (lambda x: _acosh(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Hyperbolic arccosine",
    },
    "atanh": {
        "func": (lambda x: _atanh(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Hyperbolic arctangent",
    },
    "sqrt": {
        "func": (lambda x: _sqrt(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Square root",
    },
    "gcd": {
        "func": (lambda x1, x2: _gcd(x1, x2)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Greatest common divisor",
    },
    "lcm": {
        "func": (lambda x1, x2: _lcm(x1, x2)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Least common multiple",
    },
    "radians": {
        "func": (lambda deg: _radians(deg)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Convert degrees to radians",
    },
    "!": {
        "func": (lambda x: _factorial(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Factorial",
    },
    "ceil": {
        "func": (lambda x: _ceil(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Ceiling",
    },
    "floor": {
        "func": (lambda x: _floor(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Floor",
    },
    "comb": {
        "func": (lambda n, k: _comb(n, k)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Combinations",
    },
    "perm": {
        "func": (lambda n, k: _perm(n, k)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Permutations",
    },
    "abs": {
        "func": (lambda x: _abs(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Absolute value",
    },
    "cbrt": {
        "func": (lambda x: _cbrt(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Cube root",
    },
    "ncr": {
        "func": (lambda n, k: _ncr(n, k)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Combinations",
    },
    "npr": {
        "func": (lambda n, k: _npr(n, k)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Permutations",
    },
    "roundn": {
        "func": (lambda x1, x2: _roundn(x1, x2)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Round to n decimal places",
    },
    "round": {
        "func": (lambda x: _round(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Round to nearest integer",
    },
    "frac": {
        "func": (lambda a, b: _frac(a, b)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Fraction",
    },
}


--- stacker/stacker/operators/exit.py ---
import sys


exit_operators = {
    "exit": {
        "func": (lambda: sys.exit(0)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Exits the program.",
    },
    "abort": {
        "func": (lambda: sys.exit(1)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Aborts the program.",
    },
    "exit-code": {
        "func": (lambda x: sys.exit(x)),
        "arg_count": 1,
        "push_result_to_stack": False,
        "desc": "Exits the program with the given exit code.",
    },
}


--- stacker/stacker/operators/setting.py ---
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stacker.stacker import Stacker


def _disable_plugin(stacker: Stacker, operator_name: str) -> None:
    if operator_name in stacker.plugins:
        del stacker.plugins[operator_name]
    else:
        print(f"Plugin '{operator_name}' is not registered.")


def _disable_all_plugins(stacker: Stacker) -> None:
    stacker.plugins = {}


settings_operators = {
    "disable_plugin": {
        "func": (
            lambda stacker, operator_name: _disable_plugin(stacker, operator_name)
        ),
        "arg_count": 1,
        "push_result_to_stack": False,
        "desc": "Disables a plugin.",
    },
    "disable_all_plugins": {
        "func": (lambda stacker: _disable_all_plugins(stacker)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Disables all plugins.",
    },
}


--- stacker/stacker/operators/string.py ---
from __future__ import annotations


# def _contains(value1: str, value2: str) -> bool:
#     """Returns whether the first string contains the second string."""
#     return value2 in value1


# def _endswith(value1: str, value2: str) -> bool:
#     """Returns whether the first string ends with the second string."""
#     return value1.endswith(value2)


# def _startswith(value1: str, value2: str) -> bool:
#     """Returns whether the first string starts with the second string."""
#     return value1.startswith(value2)


# def _find(value1: str, value2: str) -> int:
#     """Returns the index of the first occurrence of the second string in the first string."""
#     return value1.find(value2)


# def _join(value1: str, value2: str) -> str:
#     """Concatenate two strings."""
#     return value1.join(value2)


string_operators = {
    "asc": {
        "func": (lambda value: ord(value)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Returns the ASCII value of the specified character.",
    },
    "chr": {
        "func": (lambda value: chr(value)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Returns the character that matches the specified ASCII value.",
    },
    "concat": {
        "func": (lambda value1, value2: value1 + value2),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Concatenate two strings.",
    },
    "search": {
        "func": (lambda value1, value2: value1.find(value2)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Returns the index of the first occurrence of the second string in the first string.",
    },
    "replace": {
        "func": (lambda value1, value2, value3: value1.replace(value2, value3)),
        "arg_count": 3,
        "push_result_to_stack": True,
        "desc": "Replaces all occurrences of the second string with the third string in the first string.",
    },
    "lower": {
        "func": (lambda value: value.lower()),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Converts the specified string to lowercase.",
    },
    "upper": {
        "func": (lambda value: value.upper()),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Converts the specified string to uppercase.",
    },
    "title": {
        "func": (lambda value: value.title()),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Converts the specified string to title case.",
    },
    "strip": {
        "func": (lambda value: value.strip()),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Removes leading and trailing whitespace from the specified string.",
    },
    "lstrip": {
        "func": (lambda value: value.lstrip()),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Removes leading whitespace from the specified string.",
    },
    "rstrip": {
        "func": (lambda value: value.rstrip()),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Removes trailing whitespace from the specified string.",
    },
    # "split": {
    #     "func": (lambda value1, value2: value1.split(value2)),
    #     "arg_count": 2,
    #     "push_result_to_stack": True,
    #     "desc": "Splits the specified string into a list of substrings using the specified delimiter.",
    # },
    "join": {
        "func": (lambda value1, value2: value2.join(value1)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Concatenates the elements of the specified list using the specified delimiter.",
    },
    # "len": {
    #     "func": (lambda value: len(value)),
    #     "arg_count": 1,
    #     "push_result_to_stack": True,
    #     "desc": "Returns the length of the specified string.",
    # },
    "contains": {
        "func": (lambda value1, value2: value2 in value1),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Returns whether the first string contains the second string.",
    },
    "subseq": {
        "func": (lambda value: value.split()[0]),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Returns a substring of the specified string.",
    },
    "format": {
        "func": (lambda value1, value2: value1.format(value2)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Formats the specified string using the specified arguments.",
    },
}


--- stacker/stacker/operators/lmd.py ---
from __future__ import annotations

from stacker.engine.slambda import StackerLambda


lambda_operators = {
    "lambda": {
        "func": lambda fargs, body: StackerLambda(fargs, body),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Defines a function.",
    },
}


--- stacker/stacker/operators/system.py ---
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stacker.engine.core import StackerCore


def _vars(core: StackerCore) -> None:
    """
    Display all defined variables.
    Example:
        stacker> 5 $x set
        stacker> 10 $y set
        stacker> vars
        x = 5
        y = 10
    """
    variables = core.variables
    if len(variables) == 0:
        print("No variables defined.")
        return
    for key, value in variables.items():
        print(f"{key} = {value}")


def _funcs(core: StackerCore) -> None:
    """
    Display all defined functions.
    Example:
        stacker> {x} {x x *} $square defun
        stacker> funcs
        square: {x} {x x *}
    """
    functions = core.sfunctions
    if len(functions) == 0:
        print("No functions defined.")
        return
    for name, func_dict in functions.items():
        func = func_dict["func"]
        print(f"{name}: args={func.args}, body={func.blockstack}")


def _macros(core: StackerCore) -> None:
    """
    Display all defined macros.
    Example:
        stacker> {x} {x x *} $square defmacro
        stacker> macros
        square: {x} {x x *}
    """
    macros = core.macros
    if len(macros) == 0:
        print("No macros defined.")
        return
    for name, macro in macros.items():
        print(f"{name}: {macro.blockstack}")


def _operators(core: StackerCore) -> None:
    """
    Display all available operators grouped by category.
    Example:
        stacker> operators
        Regular operators:
          +: Addition
          -: Subtraction
          ...
        Stack operators:
          dup: Duplicate top of stack
          ...
    """
    print("Regular operators:")
    regular_ops = {}
    regular_ops.update(core.operator_manager.get_regular_descriptions())
    regular_ops.update(core.operator_manager.get_priority_descriptions())
    for name, desc in regular_ops.items():
        print(f"  {name}: {desc}")

    print("\nStack operators:")
    for name, desc in core.operator_manager.get_stack_descriptions().items():
        print(f"  {name}: {desc}")

    print("\nSettings operators:")
    for name, desc in core.operator_manager.get_settings_descriptions().items():
        print(f"  {name}: {desc}")

    print("\nSystem operators:")
    for name, desc in core.operator_manager.get_system_descriptions().items():
        print(f"  {name}: {desc}")


# Export operators
system_operators = {
    "vars": {
        "func": (lambda stack, core: _vars(core)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Display all defined variables.",
    },
    "funcs": {
        "func": (lambda stack, core: _funcs(core)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Display all defined functions.",
    },
    "macros": {
        "func": (lambda stack, core: _macros(core)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Display all defined macros.",
    },
    "operators": {
        "func": (lambda stack, core: _operators(core)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Display all available operators.",
    },
}


--- stacker/stacker/operators/defmacro.py ---
from __future__ import annotations

from typing import TYPE_CHECKING

from stacker.engine.smacro import StackerMacro

if TYPE_CHECKING:
    from stacker.stacker import Stacker


def define_macro(stacker: Stacker, name: str, body: Stacker) -> None:
    """Defines a macro."""
    macro = StackerMacro(name, body)
    stacker.register_macro(name, macro)


macro_operators = {
    "defmacro": {
        "func": (lambda stacker, name, body: define_macro(stacker, name, body)),
        "arg_count": 2,
        "push_result_to_stack": False,
        "desc": "Defines a macro.",
    },
}


--- stacker/stacker/operators/file.py ---
from __future__ import annotations

from typing import Any
from pathlib import Path
import os


def _write(content, filename: Path | str) -> None:
    filename = Path(filename).resolve()
    with open(filename, "w") as f:
        f.write(content)


def _read(filename: Path | str) -> str | None:
    filename = Path(filename).resolve()
    if not filename.is_file():
        raise FileNotFoundError(f"File {filename} not found.")
    if not filename.exists():
        raise FileNotFoundError(f"File {filename} does not exist.")
    with open(filename, "r") as f:
        return f.read()


class FileIterator:
    def __init__(self, filename: str, mode: str = "r"):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

    def readline(self):
        if self.file:
            line = self.file.readline()
            if line:
                return line.rstrip("\n")
            return None
        return None


def write_to_file(data: Any, filename: str) -> None:
    """Write data to a file"""
    with open(filename, "w") as f:
        f.write(str(data))


def read_from_file(filename: str) -> str:
    """Read all content from a file"""
    content = None
    with open(filename, "r") as f:
        content = f.read()
    return content


def append_to_file(data: Any, filename: str) -> None:
    """Append data to a file"""
    with open(filename, "a") as f:
        f.write(str(data))


def read_lines_from_file(filename: str) -> list[str]:
    """Read all lines from a file"""
    lines = []
    with open(filename, "r") as f:
        lines = [line.rstrip("\n") for line in f]
    return lines


def file_exists(filename: str) -> bool:
    """Check if a file exists"""
    exists = os.path.exists(filename)
    return exists


file_operators = {
    "write-to-file": {
        "func": (lambda data, filename: write_to_file(data, filename)),
        "arg_count": 2,
        "push_result_to_stack": False,
        "desc": "Write data to file",
    },
    "append-to-file": {
        "func": (lambda filename, content: append_to_file(filename, content)),
        "arg_count": 2,
        "push_result_to_stack": False,
        "desc": "Append content to file",
    },
    "read-lines": {
        "func": (lambda filename: read_lines_from_file(filename)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Read all lines from file",
    },
    "read-from-file": {
        "func": (lambda filename: read_from_file(filename)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Read all content from file",
    },
    "file-exists": {
        "func": (lambda filename: file_exists(filename)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Check if file exists",
    },
}


--- stacker/stacker/operators/base.py ---
from __future__ import annotations

import re


def _convert_to_base(value: str | int, base: int) -> str | int:
    value = str(value)

    # Binary (0b...)
    binary_pattern = re.compile(r"^0b[01]+$")
    # octal (0o...)
    octal_pattern = re.compile(r"^0o[0-7]+$")
    # decimal
    decimal_pattern = re.compile(r"^[-+]?\d+$")
    # hexadecimal (0x...)
    hex_pattern = re.compile(r"^0x[\da-fA-F]+$")

    if not (
        binary_pattern.match(value)
        or octal_pattern.match(value)
        or decimal_pattern.match(value)
        or hex_pattern.match(value)
    ):
        raise ValueError("Invalid number format.(convert_to_base)")

    value_as_int = int(value, 0)
    # 0 means that binary, octal, and hexadecimal numbers are automatically detected and processed

    if base == 2:
        return bin(value_as_int)
    elif base == 8:
        return oct(value_as_int)
    elif base == 10:
        return value_as_int
    elif base == 16:
        return hex(value_as_int)
    else:
        raise ValueError("Invalid base.")


base_operators = {
    "bin": {
        "func": (lambda value: _convert_to_base(value, 2)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Binary representation",
    },
    "oct": {
        "func": (lambda value: _convert_to_base(value, 8)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Octal representation",
    },
    "dec": {
        "func": (lambda value: _convert_to_base(value, 10)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Decimal representation",
    },
    "hex": {
        "func": (lambda value: _convert_to_base(value, 16)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Hexadecimal representation",
    },
}


--- stacker/stacker/operators/stack.py ---
from __future__ import annotations

import itertools

from collections import deque
from typing import Any
from stacker.error import (
    DropError,
    DupError,
    OverError,
    SwapError,
    RollError,
    RotError,
    PickError,
    NipError,
    InsertError,
)
from stacker.util.disp import disp_stack


"""
Stack manipulation functions.

stack = ['a', 'b', 'c', 'd']

index: value
    4: 'a'
    3: 'b'
    2: 'c'
    1: 'd' <- top
"""


def _drop(stack: deque | list) -> None:
    """
    Drops the top element of the stack.
    Example:
        # 3: 'a'  |
        # 2: 'b'  | 2: 'a'
        # 1: 'c'  | 1: 'b'
    """
    if len(stack) == 0:
        raise DropError("Stack is empty")
    stack.pop()


def _drop2(stack: deque | list) -> None:
    """
    Drops the top two elements of the stack.
    Example:
        # 4: 'a'  |
        # 3: 'b'  |
        # 2: 'c'  | 2: 'a'
        # 1: 'd'  | 1: 'b'
    """
    if len(stack) < 2:
        raise DropError("Stack has less than 2 elements")
    stack.pop()
    stack.pop()


def _dropn(num: int, stack: deque | list) -> None:
    """
    Drops the top n elements of the stack.
    Example:
        # 6: 'a'  |
        # 5: 'b'  |
        # 4: 'c'  |
        # 3: 'd'  |
        # 2: 'e'  | 2: 'a'
        # 1: 3    | 1: 'b'
    """
    if len(stack) == 0:
        raise DropError("Stack is empty")
    if num > len(stack):
        raise DropError("Num is greater than stack size")
    for _ in range(num):
        stack.pop()


def _dup(stack: deque | list) -> None:
    """
    Duplicates the top element of the stack.
    Example:
        # 2:      | 2: 'a'
        # 1: 'a'  | 1: 'a'
    """
    if len(stack) == 0:
        raise DupError("Stack is empty")
    stack.append(stack[-1])


def _dup2(stack: deque | list) -> None:
    """
    Duplicates the top two elements of the stack.
    Example:
        # 4:      | 4: 'a'
        # 3:      | 3: 'b'
        # 2: 'a'  | 2: '1'
        # 1: 'b'  | 1: 'b'
    """
    if len(stack) < 2:
        raise DupError("Stack has less than 2 elements")
    start_index = len(stack) - 2
    end_index = len(stack)
    if isinstance(stack, list):
        stack.extend(stack[start_index:end_index])
    else:
        stack.extend(deque(itertools.islice(stack, start_index, end_index)))


def _dupn(num: int, stack: deque | list) -> None:
    """
    Duplicates the top n elements of the stack.
    Example:
        # 6:      | 6: 'a'
        # 5:      | 5: 'b'
        # 4: 'a'  | 4: 'c'
        # 3: 'b'  | 3: 'a'
        # 2: 'c'  | 2: 'b'
        # 1: 3    | 1: 'c'
    """
    if len(stack) == 0:
        raise DupError("Stack is empty")
    if num > len(stack):
        raise DupError("Index out of range")
    start_index = len(stack) - num
    end_index = len(stack)
    if isinstance(stack, list):
        stack.extend(stack[start_index:end_index])
    else:
        stack.extend(deque(itertools.islice(stack, start_index, end_index)))


def _over(stack: deque | list) -> None:
    """
    Copies the second element to the top of the stack.
    Example:
        # 3:     | 3: 'a'
        # 2: 'a' | 2: 'b'
        # 1: 'b' | 1: 'a'
    """
    if len(stack) < 2:
        raise OverError("Stack has less than 2 elements")
    stack.append(stack[-2])


def _swap(stack: deque | list):
    """
    Swaps the top two elements of the stack.
    Example:
        # 3: 'a'  | 3: 'a'
        # 2: 'b'  | 2: 'c'
        # 1: 'c'  | 1: 'b'
    """
    if len(stack) < 2:
        raise SwapError("Stack has less than 2 elements")
    stack[-1], stack[-2] = stack[-2], stack[-1]


def _roll(n: int, stack: deque | list) -> None:
    """
    Moves the nth element to the top of the stack.
    Example:
        # 5: 'a'  | 5: 'b'
        # 4: 'b'  | 4: 'c'
        # 3: 'c'  | 3: 'd'
        # 2: 'd'  | 2: 'a'
        # 1: 4
    """
    if len(stack) == 0:
        raise RollError("Stack is empty")
    if n > len(stack):
        raise RollError("Index out of range")
    item = stack[-n]
    stack.remove(item)
    stack.append(item)


def _rot(stack: deque | list) -> None:
    """
    Move the third element to the top of the stack.
    Example:
        # 3: 'a'  | 3: 'b'
        # 2: 'b'  | 2: 'c'
        # 1: 'c'  | 1: 'a'
    """
    if len(stack) < 3:
        raise RotError("Stack has less than 3 elements")
    stack[-1], stack[-2], stack[-3] = stack[-3], stack[-1], stack[-2]


def _unrot(stack: deque | list) -> None:
    """
    Moves the top element to the third position of the stack.
    Example:
        # 3: 'a'  | 3: 'b'
        # 2: 'b'  | 2: 'c'
        # 1: 'c'  | 1: 'a'
    """
    if len(stack) < 3:
        raise RotError("Stack has less than 3 elements")
    stack[-1], stack[-2], stack[-3] = stack[-2], stack[-3], stack[-1]


def _pick(num: int, stack: deque | list) -> None:
    """
    Copies the nth element to the top of the stack.
    Example:
        # 5: 'a'  | 5: 'a'
        # 4: 'b'  | 4: 'b'
        # 3: 'c'  | 3: 'c'
        # 2: 'd'  | 2: 'd'
        # 1: 2    | 1: 'c'
    """
    if len(stack) == 0:
        raise PickError("Stack is empty")
    elif num >= len(stack):
        raise PickError("Index out of range")
    if num < 0:
        num = len(stack) + num + 1
    index = len(stack) - num
    stack.append(stack[index])


def _nip(stack: deque | list) -> None:
    """
    Removes the second element from the top of the stack.
    Example:
        # 3: 'a'  | 3:
        # 2: 'b'  | 2: 'a'
        # 1: 'c'  | 1: 'c'
    """
    if len(stack) < 2:
        raise NipError("Stack has less than 2 elements")
    stack.remove(stack[-2])


def _depth(stack: deque | list) -> int:
    """
    Returns the depth of the stack.
    Example:
        # 4:      | 4: 'a'
        # 3: 'a'  | 3: 'b'
        # 2: 'b'  | 2: 'c'
        # 1: 'c'  | 1: 3
    """
    return len(stack)


def _insert(index: int, value: Any, stack: deque | list) -> None:
    """
    Inserts a value at the specified index.
    Example:
        # 6: 'a'  | 6:
        # 5: 'b'  | 5: 'a'
        # 4: 'c'  | 4: 'b'
        # 3: 'd'  | 3: 'e'
        # 2: 2    | 2: 'c'
        # 1: 'e'  | 1: 'd'
    """
    index = len(stack) - index
    if index > len(stack):
        raise InsertError("index out of range")
    stack.insert(index, value)


def _rev(stack: deque | list) -> None:
    """
    Reverses the stack.
    Example:
        # 4: 'a'  | 4: 'd'
        # 3: 'b'  | 3: 'c'
        # 2: 'c'  | 2: 'b'
        # 1: 'd'  | 1: 'a'
    """
    stack.reverse()


def _count(
    value: Any,
    stack: deque | list,
) -> int:
    """
    Counts the number of occurrences of a value in the stack.
    """
    return stack.count(value)


def _clear(stack: deque | list) -> None:
    """
    Clears the stack.
    """
    stack.clear()


def _disp(stack: deque | list) -> None:
    """
    Prints the stack.
    """
    if isinstance(stack, deque):
        # print(list(stack))
        disp_stack(list(stack))
    else:
        # print(stack)
        disp_stack(stack)


stack_operators = {
    "drop": {
        "func": (lambda stack: _drop(stack)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Drops the top element of the stack.",
    },
    "drop2": {
        "func": (lambda stack: _drop2(stack)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Drops the top two elements of the stack.",
    },
    "dropn": {
        "func": (lambda num, stack: _dropn(num, stack)),
        "arg_count": 1,
        "push_result_to_stack": False,
        "desc": "Drops the top n elements of the stack.",
    },
    "dup": {
        "func": (lambda stack: _dup(stack)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Duplicates the top element of the stack.",
    },
    "dup2": {
        "func": (lambda stack: _dup2(stack)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Duplicates the top two elements of the stack.",
    },
    "dupn": {
        "func": (lambda num, stack: _dupn(num, stack)),
        "arg_count": 1,
        "push_result_to_stack": False,
        "desc": "Duplicates the top n elements of the stack.",
    },
    "over": {
        "func": (lambda stack: _over(stack)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Copies the second element to the top of the stack.",
    },
    "swap": {
        "func": (lambda stack: _swap(stack)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Swaps the top two elements of the stack.",
    },
    "pick": {
        "func": (lambda num, stack: _pick(num, stack)),
        "arg_count": 1,
        "push_result_to_stack": False,
        "desc": "Copies the nth element to the top of the stack.",
    },
    "roll": {
        "func": (lambda num, stack: _roll(num, stack)),
        "arg_count": 1,
        "push_result_to_stack": False,
        "desc": "Moves the nth element to the top of the stack.",
    },
    "rot": {
        "func": (lambda stack: _rot(stack)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Move the third element to the top of the stack.",
    },
    "unrot": {
        "func": (lambda stack: _unrot(stack)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Moves the top element to the third position of the stack.",
    },
    "nip": {
        "func": (lambda stack: _nip(stack)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Removes the second element from the top of the stack.",
    },
    "depth": {
        "func": (lambda stack: _depth(stack)),
        "arg_count": 0,
        "push_result_to_stack": True,
        "desc": "Returns the depth of the stack.",
    },
    "ins": {
        "func": (lambda index, value, stack: _insert(index, value, stack)),
        "arg_count": 2,
        "push_result_to_stack": False,
        "desc": "Inserts a element at the specified index.",
    },
    "rev": {
        "func": (lambda stack: _rev(stack)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Reverses the stack.",
    },
    "count": {
        "func": (lambda stack, value: _count(stack, value)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Counts the number of occurrences of a value in the stack.",
    },
    "clear": {
        "func": (lambda stack: _clear(stack)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Clears the stack.",
    },
    "disp": {
        "func": (lambda stack: _disp(stack)),
        "arg_count": 0,
        "push_result_to_stack": False,
        "desc": "Prints the stack.",
    },
}


--- stacker/stacker/operators/types.py ---
from __future__ import annotations


type_operators = {
    "int": {
        "func": (lambda x: int(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Convert to int",
    },
    "float": {
        "func": (lambda x: float(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Convert to float",
    },
    "str": {
        "func": (lambda x: str(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Convert to str",
    },
    "bool": {
        "func": (lambda x: bool(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Convert to bool",
    },
    "complex": {
        "func": (lambda x: complex(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Convert to complex",
    },
    "type": {
        "func": (lambda x: type(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Get type",
    },
}


--- stacker/stacker/operators/transform.py ---
from __future__ import annotations


transform_operators = {
    "enumerate": {
        "func": (lambda xs: enumerate(xs)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Enumerates a list.",
    },
    "sorted": {
        "func": (lambda xs: sorted(xs)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Sorts a list.",
    },
    "reversed": {
        "func": (lambda xs: reversed(xs)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Reverses a list.",
    },
    "list": {
        "func": (lambda x: list(x)),
        "arg_count": 1,
        "push_result_to_stack": True,
        "desc": "Converts an iterable to a list.",
    },
    # REMOVED: "tuple" operator - () now creates code blocks, not tuples
    # Use lists [] instead of tuples for data structures
}


--- stacker/stacker/operators/hof.py ---
##############################################################################
# Higher-order functions
##############################################################################


from __future__ import annotations


from functools import reduce as py_reduce


hof_operators = {
    "map": {
        "func": (lambda func, xs: map(func, xs)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Applies a function to each element of a list.",
    },
    "filter": {
        "func": (lambda func, xs: filter(func, xs)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Filters a list based on a predicate function.",
    },
    "zip": {
        "func": (lambda xs, ys: zip(xs, ys)),
        "arg_count": 2,
        "push_result_to_stack": True,
        "desc": "Zips two lists together.",
    },
    "reduce": {
        "func": (lambda func, init, xs: py_reduce(func, xs, init)),
        "arg_count": 3,
        "push_result_to_stack": True,
        "desc": "Reduces a list to a single value using a binary function.",
    },
    "fold": {
        "func": (lambda func, init, xs: py_reduce(func, xs, init)),
        "arg_count": 3,
        "push_result_to_stack": True,
        "desc": "Alias for reduce. Folds a list to a single value using a binary function.",
    },
}


--- stacker/stacker/include/include.py ---
from __future__ import annotations

from pathlib import Path

from stacker.error import IncludeError
from stacker.include.stk_file_read import readtxt
from stacker.syntax.parser import remove_start_end_quotes


def include_stacker_script(filename: str | Path):
    """Import a stacker script and return the stacker object."""
    if isinstance(filename, str):
        filename = remove_start_end_quotes(filename)
        # filename = Path(filename).resolve()
        filename = Path(filename)
    if not filename.is_file():
        raise IncludeError(f"File {filename} not found.")
    if not filename.exists():
        raise IncludeError(f"File {filename} not found.")
    if filename.suffix != ".stk":
        raise IncludeError(f"File {filename} is not a stacker script.")

    # with open(filename, 'r') as file:
    # script_content = file.read()

    script_content = readtxt(filename)

    from stacker.stacker import Stacker

    stacker = Stacker()
    stacker.process_expression(script_content)
    return stacker


--- stacker/stacker/include/__init__.py ---
from __future__ import annotations

from stacker.include.include import include_stacker_script

__all__ = ["include_stacker_script"]


--- stacker/stacker/include/stk_file_read.py ---
def readtxt(file_path):
    """
    This function reads a text file and ignores lines that are either
    within triple double quotes (\"\"\")
    within triple single quotes (''')
    start with a hash (#)
    or are blank lines (including the last line if it's blank).
    Additionally, it trims a final newline character if it exists.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    # State flags to track if the current line is within a block comment
    in_double_quote_comment = False
    in_single_quote_comment = False

    filtered_lines = []

    for line in lines:
        if line.strip().startswith(
            '"""'
        ):  # Check for the start and end of triple double quote block
            in_double_quote_comment = not in_double_quote_comment
            continue  # Skip the line with triple quotes
        if line.strip().startswith(
            "'''"
        ):  # Check for the start and end of triple single quote block
            in_single_quote_comment = not in_single_quote_comment
            continue  # Skip the line with triple quotes
        if (
            in_double_quote_comment or in_single_quote_comment
        ):  # Skip lines within block comments
            continue
        # if (
        #     line.strip().startswith("#") or not line.strip()
        # ):  # Skip lines that start with # or are blank lines (including the last line if it's blank)
        #     continue
        filtered_lines.append(line)

    # Trim the final newline character if it exists
    if filtered_lines and not filtered_lines[-1].strip():
        filtered_lines.pop()

    return "".join(filtered_lines).rstrip(
        "\n"
    )  # Remove trailing newline if it's the last character


--- stacker/stacker/engine/scope.py ---
"""
Variable scope implementation using parent chain for efficient lookups.

This module provides a scope chain mechanism to avoid deep copying of variables
during function calls, significantly improving performance while maintaining
correct scoping semantics.
"""

from __future__ import annotations
from typing import Any, Iterator


class ScopedVariables:
    """
    Variable scope with parent chain for efficient variable lookup.

    This class implements lexical scoping using a parent chain, similar to
    how JavaScript, Python, and many other languages handle variable scopes.

    When a variable is accessed:
    1. Check local scope first
    2. If not found, check parent scope
    3. Continue up the chain until found or reach root

    When a variable is set:
    1. Always set in the local scope only

    This avoids the need for deep copying entire variable dictionaries.
    """

    def __init__(
        self, parent: ScopedVariables | None = None, local_vars: dict | None = None
    ):
        """
        Initialize a new scope.

        Args:
            parent: Parent scope (None for root scope)
            local_vars: Initial local variables (default: empty dict)
        """
        self._local: dict[str, Any] = local_vars if local_vars is not None else {}
        self._parent: ScopedVariables | None = parent

    def __getitem__(self, key: str) -> Any:
        """
        Get a variable value, searching up the scope chain.

        Args:
            key: Variable name

        Returns:
            Variable value

        Raises:
            KeyError: If variable is not found in any scope
        """
        if key in self._local:
            return self._local[key]
        elif self._parent is not None:
            return self._parent[key]
        else:
            raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set a variable in the current scope only.

        Args:
            key: Variable name
            value: Variable value
        """
        self._local[key] = value

    def set_global(self, key: str, value: Any) -> None:
        """
        Set a variable in the global (root) scope.

        Traverses up to the root scope and sets the variable there.

        Args:
            key: Variable name
            value: Variable value
        """
        if self._parent is None:
            # We are at the root (global) scope
            self._local[key] = value
        else:
            # Recurse up to the root
            self._parent.set_global(key, value)

    def update_existing(self, key: str, value: Any) -> bool:
        """
        Update an existing variable by searching up the scope chain.

        If the variable exists in any scope, update it there.
        If it doesn't exist anywhere, do nothing and return False.

        Args:
            key: Variable name
            value: Variable value

        Returns:
            True if variable was found and updated, False otherwise
        """
        if key in self._local:
            # Found in local scope, update it
            self._local[key] = value
            return True
        elif self._parent is not None:
            # Recurse to parent scope
            return self._parent.update_existing(key, value)
        else:
            # Not found anywhere
            return False

    def __delitem__(self, key: str) -> None:
        """
        Delete a variable from the current scope only.

        Args:
            key: Variable name

        Raises:
            KeyError: If variable is not in local scope
        """
        del self._local[key]

    def __contains__(self, key: str) -> bool:
        """
        Check if a variable exists, searching up the scope chain.

        Args:
            key: Variable name

        Returns:
            True if variable exists in any scope
        """
        return key in self._local or (self._parent is not None and key in self._parent)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a variable value with a default, searching up the scope chain.

        Args:
            key: Variable name
            default: Default value if not found

        Returns:
            Variable value or default
        """
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: str, default: Any = None) -> Any:
        """
        Remove and return a variable from the local scope only.

        Args:
            key: Variable name
            default: Default value if not found

        Returns:
            Variable value or default
        """
        return self._local.pop(key, default)

    def keys(self) -> Iterator[str]:
        """
        Get all variable names from all scopes.

        Yields:
            Variable names
        """
        # Yield local keys first
        yield from self._local.keys()
        # Then parent keys (avoiding duplicates)
        if self._parent is not None:
            for key in self._parent.keys():
                if key not in self._local:
                    yield key

    def items(self) -> Iterator[tuple[str, Any]]:
        """
        Get all variable name-value pairs from all scopes.

        Yields:
            (name, value) tuples
        """
        # Yield local items first
        yield from self._local.items()
        # Then parent items (avoiding duplicates)
        if self._parent is not None:
            for key, value in self._parent.items():
                if key not in self._local:
                    yield key, value

    def update(self, other: dict) -> None:
        """
        Update local scope with variables from a dict.

        Args:
            other: Dictionary of variables to add
        """
        self._local.update(other)

    def __len__(self) -> int:
        """
        Get the total number of unique variables across all scopes.

        Returns:
            Number of unique variables
        """
        # Count unique keys across all scopes
        all_keys = set(self.keys())
        return len(all_keys)

    def create_child_scope(self) -> ScopedVariables:
        """
        Create a new child scope with this scope as parent.

        Returns:
            New child scope
        """
        return ScopedVariables(parent=self)

    def copy(self) -> ScopedVariables:
        """
        Create a shallow copy of this scope (local variables only).

        The copy will have the same parent as this scope.

        Returns:
            New scope with copied local variables
        """
        return ScopedVariables(parent=self._parent, local_vars=self._local.copy())

    def __repr__(self) -> str:
        """String representation for debugging."""
        local_vars = dict(self._local)
        has_parent = self._parent is not None
        return f"ScopedVariables(local={local_vars}, has_parent={has_parent})"


--- stacker/stacker/engine/core.py ---
from __future__ import annotations
import copy
from typing import TYPE_CHECKING, Any
import ast
from functools import lru_cache
from stacker.constant import constants
from stacker.error import (
    StackUnderflowError,
    StackerSyntaxError,
    UndefinedSymbolError,
    # UnexpectedTokenError,
)
from stacker.syntax.parser import (
    convert_custom_array_to_proper_list,
    is_block,
    is_code_block,
    # is_contains_transpose_command,
    # is_label_symbol,
    is_string,
    is_list,
    # is_transpose_command,
    # is_tuple,  # REMOVED: Tuples no longer supported, () now creates code blocks
    is_symbol,
    parse_expression,
)
from stacker.reserved import (
    __BREAK__,
    # __TRANSPOSE__
)
from stacker.engine.data_type import String, stack_data, VOID
from stacker.engine.slambda import StackerLambda
from stacker.engine.scope import ScopedVariables
from stacker.operators.manager import OperatorManager

if TYPE_CHECKING:
    # from stacker.engine.sfunction import StackerFunction
    from stacker.engine.smacro import StackerMacro


# Cache for literal_eval to avoid re-evaluating the same tokens
@lru_cache(maxsize=1024)
def _cached_literal_eval(token: str) -> Any:
    """Cached version of ast.literal_eval for performance."""
    try:
        return ast.literal_eval(token)
    except Exception:
        return token


class StackerCore:
    """A class for evaluating RPN expressions."""

    def __init__(
        self, expression: str | None = None, parent: StackerCore | None = None
    ):
        self.parent = parent
        self.child = None
        self.trace: list[Any] = []  # for error trace
        self.stack: stack_data[Any] = stack_data()
        self.tokens = []
        self.bracket_type = "{"  # Default bracket type for display ({} or ())

        # Source location tracking for error reporting
        self.current_file: str | None = None
        self.current_line: int | None = None
        self.source_lines: dict[int, str] = {}  # Map line number to source code

        if self.parent is not None:  # it is a substack of a parent stacker
            self.operator_manager = self.parent.operator_manager
            self.macros = self.parent.macros
            self.variables = self.parent.variables
            self.plugins = self.parent.plugins
            self.sfunctions = self.parent.sfunctions
            self.labels = self.parent.labels
            # Share source location tracking with parent
            self.current_file = self.parent.current_file
            self.current_line = self.parent.current_line
            self.source_lines = self.parent.source_lines
            if expression is not None:
                self.tokens = list(
                    map(self._block_token_format, parse_expression(expression))
                )
            return

        if expression is not None and self.parent is None:
            raise NotImplementedError

        self.operator_manager = OperatorManager()
        # Use ScopedVariables for efficient variable scoping
        self.variables = ScopedVariables(local_vars=dict(constants))
        self.sfunc_args = {}
        self.macros = {}
        self.plugins = {}
        self.sfunctions = {}
        self.labels = {}

    def _block_token_format(self, token: str) -> str:
        # Check if token is a nested code block
        if is_code_block(token):
            # Convert to StackerCore instance
            temp_stack = stack_data()
            self._substack(token, temp_stack)
            return temp_stack.pop()
        # For non-code-block tokens, evaluate to preserve proper types
        # but don't resolve variables (keep them as strings for lazy evaluation)
        if token in self.operator_manager.operators["regular"]:
            return self._literal_eval2(f'"{token}"')
        # Try to evaluate as literal (numbers, strings, etc.)
        # but fallback to string if it's an identifier
        try:
            if (token.startswith("'") and token.endswith("'")) or (
                token.startswith('"') and token.endswith('"')
            ):
                return String(token[1:-1])
            else:
                return _cached_literal_eval(token)
        except Exception:
            # Keep as string for lazy evaluation (variables, operators, etc.)
            return token

    def _substack(self, token: str, stack: stack_data) -> None:
        """Creates a substack from a code block.

        :param token: Code block with {...} or (...) delimiters.
        """
        # Strip delimiters and remember bracket type for display
        if token.startswith("{") and token.endswith("}"):
            expression = token[1:-1]
            bracket_type = "{"
        elif token.startswith("(") and token.endswith(")"):
            expression = token[1:-1]
            bracket_type = "("
        else:
            raise ValueError(f"Invalid code block: {token}")

        self.child = type(self)(expression=expression, parent=self)
        self.child.bracket_type = bracket_type
        stack.append(self.child)

    def _substack_with_expression(self, expression: str, stack: stack_data) -> None:
        self.child = type(self)(expression=expression, parent=self)
        stack.append(self.child)

    def _substack_with_tokens(self, tokens: list, stack: stack_data) -> None:
        self.child = type(self)(parent=self)
        self.child.tokens = tokens
        stack.append(self.child)

    def _safe_pop(self, stack: stack_data, operator: str = "unknown", num_args: int = 1) -> Any:
        """Safely pop from stack with informative error messages.

        Args:
            stack: The stack to pop from
            operator: Name of the operator requesting the pop (for error messages)
            num_args: Number of arguments the operator requires

        Returns:
            The popped value

        Raises:
            StackUnderflowError: If stack is empty
        """
        try:
            return stack.pop()
        except IndexError:
            raise StackUnderflowError(operator, num_args)

    def _pop_only(self, stack: stack_data) -> Any:
        top = stack.pop()
        self.trace.append(top)
        return

    def _pop_and_eval(self, stack: stack_data) -> Any:
        from stacker.engine.data_type import UndefinedSymbol
        from stacker.error import UndefinedSymbolError

        value = stack.pop()

        # Check if value is an UndefinedSymbol
        if isinstance(value, UndefinedSymbol):
            raise UndefinedSymbolError(value.name)

        if isinstance(value, StackerCore):
            value._evaluate(value.tokens, stack=value.stack)
            sub = value.stack
            if sub:
                stack.extend(sub)
                return stack.pop()
            else:
                # Return VOID if the code block produces no value
                # This allows void functions (functions with side effects only)
                # VOID will not be pushed to the stack, unlike None
                return VOID
        else:
            if isinstance(value, (list, tuple)):
                return value
            elif isinstance(value, String):
                return value.value
            elif value in self.variables:
                return self.variables[value]
            return self.variables.get(value, value)

    def _eval(self, expr: str, stack: stack_data = stack_data()) -> stack_data:
        tokens = list(map(self._literal_eval, parse_expression(expr)))
        self._evaluate(tokens, stack=stack)
        return stack

    def _eval_block(self, block: StackerCore, stack: stack_data) -> None:
        self._evaluate(block.tokens, stack=stack)

    def _evaluate(self, tokens: list, stack: stack_data = stack_data()) -> stack_data:
        """
        Evaluates a given RPN expression.
        Returns the result of the evaluation.
        """
        self.trace = tokens
        # Commands that expect a symbol name as the preceding argument
        symbol_consuming_commands = {"set", "=", "defun", "defmacro"}

        for i, token in enumerate(tokens):
            if not isinstance(token, str):
                stack.append(token)  # Literal value
            elif token in self.macros:
                self._expand_macro(token, stack)
            # Inline is_string check for performance
            elif (token.startswith("'") and token.endswith("'")) or (
                token.startswith('"') and token.endswith('"')
            ):
                stack.append(String(token[1:-1]))
            # REMOVED: Tuple handling - () now creates code blocks like {}
            elif is_list(token):
                stack.append(
                    list(
                        map(
                            self._var_str_to_literal,
                            ast.literal_eval(
                                convert_custom_array_to_proper_list(token)
                            ),
                        )
                    )
                )
            elif is_symbol(token):
                token = token[1:]
                stack.append(token)
            # Check for code blocks (both {} and ())
            elif is_code_block(token):
                self._substack(token, stack)
            else:
                # For all other string tokens, perform lookahead to determine treatment
                next_token = tokens[i + 1] if i + 1 < len(tokens) else None
                next_next_token = tokens[i + 2] if i + 2 < len(tokens) else None
                should_treat_as_symbol = next_token in symbol_consuming_commands or (
                    is_code_block(str(next_token))
                    and next_next_token in {"do", "dolist"}
                )

                if should_treat_as_symbol:
                    # Treat as symbol name regardless of whether it's a variable or operator
                    stack.append(token)
                elif token in self.variables:
                    # Variable reference - evaluate it
                    value = self.variables[token]
                    if isinstance(value, StackerLambda):
                        args = []
                        for _ in range(value.arg_count):
                            args.insert(0, self._pop_and_eval(stack))
                        stack.append(value(*args))
                    else:
                        stack.append(value)
                elif (
                    token in self.operator_manager.built_in_operators
                    or token in self.sfunctions
                    or token in self.plugins
                ):
                    self._execute(token, stack)
                else:
                    # Try to evaluate as literal
                    evaluated = self._literal_eval(token)
                    if isinstance(evaluated, String):
                        stack.append(evaluated)
                    elif isinstance(evaluated, str):
                        # Undefined identifiers are treated as UndefinedSymbol
                        from stacker.engine.data_type import UndefinedSymbol

                        stack.append(UndefinedSymbol(evaluated))
                    else:
                        stack.append(evaluated)
        return stack

    def _var_str_to_literal(self, value: Any) -> Any:
        from stacker.engine.data_type import UndefinedSymbol

        # Inline is_string check for performance
        if isinstance(value, str) and (
            (value.startswith("'") and value.endswith("'"))
            or (value.startswith('"') and value.endswith('"'))
        ):
            return String(value[1:-1])
        elif isinstance(value, str) and is_symbol(value):
            if value[1:] in self.variables:
                return self.variables[value[1:]]
            else:
                # Return UndefinedSymbol instead of raising error
                return UndefinedSymbol(value[1:])
        elif isinstance(value, str) and value in self.variables:
            return self.variables[value]
        elif isinstance(value, str):
            # Return UndefinedSymbol instead of raising error
            return UndefinedSymbol(value)
        return value

    # Cache for common literal values (optimization)
    _literal_cache = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "true": True,
        "false": False,
        "True": True,
        "False": False,
    }

    def _literal_eval(self, token: str) -> Any:
        # Handle non-string tokens (already evaluated)
        if not isinstance(token, str):
            return token
        # Check for code blocks (both {} and ())
        if is_code_block(token):
            # Convert code block to StackerCore instance
            temp_stack = stack_data()
            self._substack(token, temp_stack)
            return temp_stack.pop()
        elif token in self.variables:
            return self.variables[token]
        # Inline is_string check for performance
        elif (token.startswith("'") and token.endswith("'")) or (
            token.startswith('"') and token.endswith('"')
        ):
            return String(token[1:-1])
        else:
            # Check cache first for common literals
            if token in StackerCore._literal_cache:
                return StackerCore._literal_cache[token]
            try:
                return ast.literal_eval(token)
            except Exception:
                return token

    def _literal_eval2(self, token: str) -> Any:
        # Check for code blocks (both {} and ())
        # token is guaranteed to be str by type hint, so no isinstance check needed
        if is_code_block(token):
            # Convert code block to StackerCore instance
            temp_stack = stack_data()
            self._substack(token, temp_stack)
            return temp_stack.pop()
        # Inline is_string check for performance
        elif (token.startswith("'") and token.endswith("'")) or (
            token.startswith('"') and token.endswith('"')
        ):
            return String(token[1:-1])
        else:
            # Use cached literal_eval for performance
            return _cached_literal_eval(token)

    def _execute(self, token: str, stack: stack_data) -> None:
        """
        Applies an operator to the top elements on the stack.
        Modifies the stack in-place.
        """
        try:
            self._execute_impl(token, stack)
        except IndexError as e:
            # Convert IndexError to StackUnderflowError with operator info
            # Get operator info if available
            arg_count = self._get_operator_arg_count(token)
            raise StackUnderflowError(token, arg_count) from e
        except TypeError as e:
            # Provide more helpful type error messages
            error_msg = str(e)
            if "unsupported operand type" in error_msg:
                raise TypeError(
                    f"Operator `{token}` received incompatible types. {error_msg}"
                ) from e
            raise

    def _get_operator_arg_count(self, token: str) -> int:
        """Get the argument count for an operator."""
        if token in self.sfunctions:
            return self.sfunctions[token]["arg_count"]
        elif token in self.plugins:
            return self.plugins[token]["arg_count"]
        elif token in self.operator_manager.operators["priority"]:
            return self.operator_manager.operators["priority"][token].get("arg_count", 0)
        elif token in self.operator_manager.operators["stack"]:
            return self.operator_manager.operators["stack"][token]["arg_count"]
        elif token in self.operator_manager.operators["system"]:
            return self.operator_manager.operators["system"][token]["arg_count"]
        elif token in self.operator_manager.operators["regular"]:
            return self.operator_manager.operators["regular"][token]["arg_count"]
        elif token in self.operator_manager.operators["hof"]:
            return self.operator_manager.operators["hof"][token]["arg_count"]
        elif token in self.operator_manager.operators["aggregate"]:
            return self.operator_manager.operators["aggregate"][token]["arg_count"]
        elif token in self.operator_manager.operators["file"]:
            return self.operator_manager.operators["file"][token]["arg_count"]
        elif token in self.operator_manager.operators["settings"]:
            return self.operator_manager.operators["settings"][token].get("arg_count", 0)
        return 1  # Default

    def _execute_impl(self, token: str, stack: stack_data) -> None:
        """
        Internal implementation of operator execution.
        IndexError and TypeError are caught by _execute and converted to better errors.
        """
        if token in self.sfunctions:  # sfunctions
            args = []
            sfunc = self.sfunctions[token]
            for _ in range(sfunc["arg_count"]):
                args.insert(0, self._pop_and_eval(stack))
            if sfunc["push_result_to_stack"]:
                result = sfunc["func"](*args)
                if result is not VOID:
                    stack.append(result)
            else:
                sfunc["func"](*args)
        elif token in self.plugins:
            args = []
            op = self.plugins[token]
            for _ in range(op["arg_count"]):
                args.insert(0, self._pop_and_eval(stack))
            if op["push_result_to_stack"]:
                result = op["func"](*args)
                if result is not VOID:
                    stack.append(result)
            else:
                op["func"](*args)
        elif token in self.operator_manager.operators["priority"]:  # priority operators
            op = self.operator_manager.operators["priority"][token]
            if token == "do":
                body = stack.pop()
                symbol = stack.pop()
                end_value = self._pop_and_eval(stack)
                start_value = self._pop_and_eval(stack)
                name = self._dollar_to_var_name(symbol)
                op["func"](start_value, end_value, name, body, self)
            elif token == "dolist":
                body = stack.pop()
                symbol = stack.pop()
                lst = self._pop_and_eval(stack)
                name = self._dollar_to_var_name(symbol)
                op["func"](name, lst, body, self)
            elif token == "times":
                n_times = self._pop_and_eval(stack)
                body = stack.pop()
                op["func"](n_times, body, self)
            elif token == "break":
                stack.append(__BREAK__)
            elif token == "if":
                true_block = stack.pop()
                condition = stack.pop()
                op["func"](condition, true_block, self)
            elif token == "ifelse":
                false_block = stack.pop()
                true_block = stack.pop()
                condition = stack.pop()
                op["func"](condition, true_block, false_block, self)
            elif token == "iferror":
                catch_block = stack.pop()
                try_block = stack.pop()
                op["func"](try_block, catch_block, self)
            elif token == "set" or token == "=":
                symbol = stack.pop()
                name = self._dollar_to_var_name(symbol)
                value = self._pop_and_eval(stack)
                # Try to update existing variable in scope chain
                # If not found, create in local scope
                if not self.variables.update_existing(name, value):
                    self.variables[name] = value
            elif token == "global":
                # RPN: value varname global
                # Stack: [..., value, varname]
                symbol = stack.pop()  # Pop varname
                name = self._dollar_to_var_name(symbol)
                value = self._pop_and_eval(stack)  # Pop and eval value
                # Always set in global (root) scope
                self.variables.set_global(name, value)
            elif token == "defun":
                symbol = stack.pop()
                name = self._dollar_to_var_name(symbol)
                body = stack.pop()
                fargs = stack.pop()  # str
                if isinstance(fargs, tuple):
                    fargs = list(fargs)
                elif isinstance(fargs, list):
                    fargs = fargs
                elif isinstance(fargs, StackerCore):
                    fargs = fargs.tokens
                else:
                    fargs = [fargs]
                op["func"](self, name, fargs, body)
            elif token == "defmacro":
                symbol = stack.pop()
                body = stack.pop()
                name = self._dollar_to_var_name(symbol)
                op["func"](self, name, body)
            elif token == "lambda":
                body = stack.pop()
                fargs = stack.pop()
                if op["push_result_to_stack"]:
                    result = op["func"](fargs, body)
                    if result is not VOID:
                        stack.append(result)
                else:
                    op["func"](fargs, body)
            elif token == "eval":
                expression = stack.pop()
                if expression in self.variables:
                    expression = self.variables[expression]
                if isinstance(expression, String):
                    self._eval(expression.value, stack=stack)
                elif isinstance(expression, StackerCore):
                    self._eval_block(expression, stack=stack)
                elif isinstance(expression, StackerLambda):
                    args = []
                    for _ in range(expression.arg_count):
                        args.insert(0, self._pop_and_eval(stack))
                    stack.append(expression(*args))
                else:
                    stack.append(expression)
            elif token == "sub":
                token = stack.pop()
                self._substack_with_tokens([token], stack)
            elif token == "subn":
                n = stack.pop()
                elms = [stack.pop() for _ in range(n)]
                elms.reverse()
                self._substack_with_tokens(elms, stack)
            elif token == "listn":
                n = stack.pop()
                elms = [stack.pop() for _ in range(n)]
                elms.reverse()
                stack.append(elms)
            elif token == "read-from-string":
                self._substack_with_expression(stack.pop(), stack)
            elif token == "read":
                self._substack_with_expression(input(), stack)
            elif token == "split":
                sep = stack.pop()
                word = stack.pop()
                for string in word.split(sep):
                    stack.append(string)
            elif token == "nth":
                n = stack.pop()
                lst = stack[-1]
                if isinstance(lst, String):
                    stack.append(String(lst[n]))
                else:
                    stack.append(lst[n])
            elif token == "expand":
                iterable = stack.pop()
                if isinstance(iterable, list or tuple):
                    stack.extend(iterable)
                elif isinstance(iterable, StackerCore):
                    stack.extend(iterable.tokens)
                else:
                    raise StackerSyntaxError(f"Cannot expand {iterable}")
            elif token == "include":
                filename = stack.pop()
                op["func"](self, filename)
            elif token == "exit":
                op["func"]()
        elif token in self.operator_manager.operators["stack"]:  # stack operators
            op = self.operator_manager.operators["stack"][token]
            args = [stack]
            for _ in range(op["arg_count"]):
                args.insert(0, self._pop_and_eval(stack))
            if op["push_result_to_stack"]:
                result = op["func"](*args)
                if result is not VOID:
                    stack.append(result)
            else:
                op["func"](*args)
        elif token in self.operator_manager.operators["system"]:  # system operators
            op = self.operator_manager.operators["system"][token]
            args = [stack, self]
            for _ in range(op["arg_count"]):
                args.insert(0, self._pop_and_eval(stack))
            if op["push_result_to_stack"]:
                result = op["func"](*args)
                if result is not VOID:
                    stack.append(result)
            else:
                op["func"](*args)
        elif token in self.operator_manager.operators["regular"]:  # Other operators
            op = self.operator_manager.operators["regular"][token]
            args = []
            for _ in range(op["arg_count"]):
                args.insert(0, self._pop_and_eval(stack))
            if op["push_result_to_stack"]:
                result = op["func"](*args)
                if result is not VOID:
                    stack.append(result)
            else:
                op["func"](*args)
        elif token in self.operator_manager.operators["hof"]:  # higher-order functions
            op = self.operator_manager.operators["hof"][token]
            if token in ["map", "filter"]:
                body = stack.pop()
                args = stack.pop()
                args_org = copy.deepcopy(args)
                func = self._get_hof_func(body)
                args = args.tokens if isinstance(args, StackerCore) else args
                if op["push_result_to_stack"]:
                    lst = op["func"](func, args)
                    if isinstance(args_org, list):
                        stack.append(list(lst))
                    elif isinstance(args_org, tuple):
                        stack.append(tuple(lst))
                    else:
                        self._substack_with_tokens(list(lst), stack)
                else:
                    op["func"](func, args)
            elif token in ["reduce", "fold"]:
                body = stack.pop()
                symbol_x = stack.pop()  # Second variable name (element)
                symbol_acc = stack.pop()  # First variable name (accumulator)
                init = stack.pop()
                args = stack.pop()

                # Extract variable names (same as dolist pattern)
                name_acc = self._dollar_to_var_name(symbol_acc)
                name_x = self._dollar_to_var_name(symbol_x)

                # Create binary function with variable binding
                def reduce_func(acc, x):
                    # Create child scope for this reduction step
                    original_parent_vars = self.variables
                    original_parent_stack = self.stack
                    self.variables = self.variables.create_child_scope()
                    # Bind accumulator and element to their variable names
                    self.variables[name_acc] = acc
                    self.variables[name_x] = x
                    # Evaluate the body using a temporary stack
                    result_stack = []
                    self.stack = result_stack  # Temporarily replace stack
                    self._evaluate(body.tokens, stack=result_stack)
                    # Restore parent scope and stack
                    self.stack = original_parent_stack
                    self.variables = original_parent_vars
                    # Return the result
                    if len(result_stack) == 1:
                        return result_stack[0]
                    elif len(result_stack) == 0:
                        return None
                    return result_stack[0]

                args = args.tokens if isinstance(args, StackerCore) else args
                if op["push_result_to_stack"]:
                    result = op["func"](reduce_func, init, args)
                    stack.append(result)
                else:
                    op["func"](reduce_func, init, args)
            elif token in ["zip"]:
                xs2 = stack.pop()
                xs1 = stack.pop()
                xs_org = copy.deepcopy(xs1)
                # ys_org = copy.deepcopy(ys)
                xs2 = (
                    xs2.tokens
                    if isinstance(xs2, StackerCore)
                    else self._var_str_to_literal(xs2)
                )
                xs1 = (
                    xs1.tokens
                    if isinstance(xs1, StackerCore)
                    else self._var_str_to_literal(xs1)
                )
                if op["push_result_to_stack"]:
                    lst = op["func"](xs1, xs2)
                    if isinstance(xs_org, list):
                        stack.append(list(lst))
                    elif isinstance(xs_org, tuple):
                        stack.append(tuple(lst))
                    else:
                        self._substack_with_tokens(list(lst), stack)
                else:
                    op["func"](xs1, xs2)
            else:
                ...
        elif (
            token in self.operator_manager.operators["transform"]
        ):  # transform operators
            op = self.operator_manager.operators["transform"][token]
            args = stack.pop()
            args_org = copy.deepcopy(args)
            args = (
                args.tokens
                if isinstance(args, StackerCore)
                else self._var_str_to_literal(args)
            )
            if op["push_result_to_stack"]:
                lst = op["func"](args)
                if token == "list":
                    stack.append(list(lst))
                elif token == "tuple":
                    stack.append(tuple(lst))
                else:
                    if isinstance(args_org, list):
                        stack.append(list(lst))
                    elif isinstance(args_org, tuple):
                        stack.append(tuple(lst))
                    else:
                        self._substack_with_tokens(list(lst), stack)
            else:
                op["func"](args)
        elif (
            token in self.operator_manager.operators["aggregate"]
        ):  # aggregate operators
            op = self.operator_manager.operators["aggregate"][token]
            args = stack.pop()
            args_org = copy.deepcopy(args)
            args = (
                list(map(self._literal_eval, args.tokens))
                if isinstance(args, StackerCore)
                else self._var_str_to_literal(args)
            )
            if op["push_result_to_stack"]:
                result = op["func"](args)
                if result is not VOID:
                    stack.append(result)
            else:
                op["func"](args)
        elif token in self.operator_manager.operators["file"]:
            op = self.operator_manager.operators["file"][token]
            args = []
            for _ in range(op["arg_count"]):
                args.insert(0, self._pop_and_eval(stack))
            if op["push_result_to_stack"]:
                result = op["func"](*args)
                if result is not VOID:
                    stack.append(result)
            else:
                op["func"](*args)
        elif token in self.operator_manager.operators["settings"]:  # settings operators
            op = self.operator_manager.operators["settings"][token]
            if token == "disable_plugin":
                operator_name = stack.pop()
                op["func"](self, operator_name)
            else:
                op["func"](self)
        else:
            raise StackerSyntaxError(f"Unknown operator '{token}'")
        return

    def _dollar_to_var_name(self, symbol: str | StackerCore) -> str:
        """
        - $symbol -> symbol
        - {$symbol} -> symbol
        - symbol -> raise StackerSyntaxError
        - {symbol} -> raise StackerSyntaxError
        """
        if isinstance(symbol, str):
            if is_symbol(symbol):
                return symbol[1:]
            else:
                return symbol
        elif isinstance(symbol, StackerCore):
            if len(symbol.tokens) == 1:
                if is_symbol(symbol.tokens[0]):
                    return symbol.tokens[0][1:]
                else:
                    return symbol.tokens[0]
        raise StackerSyntaxError(f"Expected a symbol, got {symbol}")

    def _get_hof_func(self, body: str | StackerCore | StackerLambda) -> callable:
        if isinstance(body, StackerCore):
            return lambda args: self._stacker_lambda(args, body.copy())
        elif isinstance(body, StackerLambda):
            return body
        else:
            if body in self.sfunctions:
                return self.sfunctions[body]["func"]
            elif body in self.plugins:
                return self.plugins[body]["func"]
            elif body in self.operator_manager.operators["regular"]:
                return self.operator_manager.operators["regular"][body]["func"]
            else:
                raise StackerSyntaxError(f"Unknown operator '{body}'")

    def _get_reduce_func(self, body: str | StackerCore | StackerLambda) -> callable:
        """Get a binary function for reduce/fold operations."""
        if isinstance(body, StackerCore):
            def binary_func(acc, x):
                stack = []
                body_copy = body.copy()
                # Push accumulator and current element to stack
                body_copy.tokens.insert(0, acc)
                body_copy.tokens.insert(1, x)
                body_copy._evaluate(body_copy.tokens, stack=stack)
                if len(stack) == 1:
                    return stack[0]
                elif len(stack) == 0:
                    return self._substack("{}")
                return stack[0]
            return binary_func
        elif isinstance(body, StackerLambda):
            return body
        else:
            if body in self.sfunctions:
                return self.sfunctions[body]["func"]
            elif body in self.plugins:
                return self.plugins[body]["func"]
            elif body in self.operator_manager.operators["regular"]:
                return self.operator_manager.operators["regular"][body]["func"]
            else:
                raise StackerSyntaxError(f"Unknown operator '{body}'")

    # def _execute_settings(self, token: str, stack: stack_data) -> None:
    #     op = self.settings_operators[token]
    #     if token == "disable_plugin":
    #         operator_name = stack.pop()
    #         op["func"](self, operator_name)
    #     else:
    #         op["func"](self)

    def _expand_macro(self, name: str, stack: stack_data) -> None:
        """Executes a macro."""
        macro: StackerMacro = self.macros[name]
        self._evaluate(macro.blockstack.tokens, stack=stack)

    def _stacker_lambda(self, arg, body: StackerCore) -> StackerCore:
        stack = []
        body.tokens.insert(0, arg)
        body._evaluate(body.tokens, stack=stack)
        if len(stack) == 1:
            return stack[0]
        elif len(stack) == 0:
            return self._substack("{}")
        return stack

    def copy(self) -> StackerCore:
        return copy.deepcopy(self)

    def __eq__(self, other: StackerCore) -> bool:
        if isinstance(other, StackerCore):
            return self.tokens == other.tokens
        else:
            if len(self.tokens) == 0:
                return other is None
            return self.tokens == other

    def __iter__(self):
        return iter(self.tokens)

    def __len__(self):
        return len(self.tokens)

    def __getitem__(self, index):
        return self.tokens[index]

    def __str__(self):
        def format_item(item):
            if isinstance(item, StackerCore):
                return str(item)
            elif is_list(item):
                return item.replace(",", " ")
            # REMOVED: Tuple handling - () now creates code blocks
            elif isinstance(item, str):
                if item in self.operator_manager.built_in_operators:
                    return item
                elif is_code_block(item):
                    return item
                elif item in self.variables:
                    return item
                else:
                    return repr(item)
            return str(item)

        formatted_items = " ".join(map(format_item, self.tokens))
        # Use the bracket type that was used to create this code block
        if self.bracket_type == "(":
            return f"({formatted_items})"
        else:
            return f"{{{formatted_items}}}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(str(self))  # TODO Check if this is correct


--- stacker/stacker/engine/slambda.py ---
from __future__ import annotations

from typing import TYPE_CHECKING, Any
from stacker.engine.data_type import stack_data

if TYPE_CHECKING:
    from stacker.engine.core import StackerCore

import copy


class StackerLambda:
    """A callable object that represents a function defined in Stacker."""

    def __init__(self, args: list[str], blockstack: Stacker) -> None:
        self.args = args
        self.blockstack = blockstack
        self.arg_count = len(args)
        self.stack = stack_data()

    def __call__(self, *values) -> Any:
        values = list(values)
        if len(values) != len(self.args):
            raise ValueError(f"Expected {len(self.args)} arguments, got {len(values)}")
        # Use shallow copy with child scope instead of deepcopy
        # This preserves variable scope chain for nested code blocks
        blockstack = copy.copy(self.blockstack)
        blockstack.variables = self.blockstack.variables.create_child_scope()
        blockstack.stack = stack_data()

        # Update nested StackerCore instances to use the new variable scope
        self._update_nested_variables(blockstack.tokens, blockstack.variables)

        for arg, value in zip(self.args, values):
            blockstack.variables[arg] = value
        self.stack.append(blockstack)
        result = blockstack._pop_and_eval(self.stack)
        return result

    def _update_nested_variables(self, tokens, new_variables):
        """Recursively update variable references in nested StackerCore instances."""
        from stacker.engine.core import StackerCore
        for token in tokens:
            if isinstance(token, StackerCore):
                token.variables = new_variables
                # Recursively update nested code blocks
                self._update_nested_variables(token.tokens, new_variables)

    def __str__(self) -> str:
        if len(self.args) == 0:
            return "λ"
        body_str = self.blockstack.__str__()
        for arg in self.args:
            body_str = body_str.replace(f"'{arg}'", arg)
        if len(self.args) == 1:
            return f"λ{self.args[0]}." + body_str
        else:
            return "λ" + "λ".join(self.args) + "." + body_str

    def __repr__(self) -> str:
        return self.__str__()


--- stacker/stacker/engine/smacro.py ---
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stacker.stacker import Stacker


class StackerMacro:
    """A callable object that represents a macro defined in Stacker."""

    def __init__(self, name: str, blockstack: Stacker) -> None:
        self.name = name
        self.blockstack = blockstack
        self.arg_count = 0

    def __call__(self) -> Stacker:
        return self.blockstack


--- stacker/stacker/engine/__init__.py ---
from stacker.engine.core import StackerCore
from stacker.engine.data_type import String, stack_data
from stacker.engine.slambda import StackerLambda
from stacker.engine.smacro import StackerMacro
from stacker.engine.sfunction import StackerFunction

__all__ = [
    "StackerCore",
    "String",
    "stack_data",
    "StackerLambda",
    "StackerMacro",
    "StackerFunction",
]


--- stacker/stacker/engine/sfunction.py ---
from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from stacker.engine.core import StackerCore

from stacker.engine.data_type import stack_data


class StackerFunction:
    """A callable object that represents a function defined in Stacker."""

    def __init__(
        self, args: list[str], blockstack: Stacker
    ) -> None:
        self.args = args
        self.blockstack = blockstack
        self.arg_count = len(args)
        self.stack = stack_data()

    def __call__(self, *values) -> Any:
        self.stack.clear()
        values = list(values)
        if len(values) != len(self.args):
            raise ValueError(f"Expected {len(self.args)} arguments, got {len(values)}")

        # Optimization: Use scope chain instead of deepcopy
        # Create a shallow copy of blockstack with a new variable scope and stack
        # This is ~100x faster than deepcopy and supports recursion correctly
        new_blockstack = copy.copy(self.blockstack)
        new_blockstack.variables = self.blockstack.variables.create_child_scope()
        new_blockstack.stack = stack_data()  # Each call needs its own stack

        # Update nested StackerCore instances to use the new variable scope
        self._update_nested_variables(new_blockstack.tokens, new_blockstack.variables)

        # Set function arguments in the new child scope
        for arg, value in zip(self.args, values):
            new_blockstack.variables[arg] = value

        self.stack.append(new_blockstack)
        result = new_blockstack._pop_and_eval(self.stack)

        return result

    def _update_nested_variables(self, tokens, new_variables):
        """Recursively update variable references in nested StackerCore instances."""
        from stacker.engine.core import StackerCore
        for token in tokens:
            if isinstance(token, StackerCore):
                token.variables = new_variables
                # Recursively update nested code blocks
                self._update_nested_variables(token.tokens, new_variables)


--- stacker/stacker/engine/data_type.py ---
from collections import deque

# class Operator:
#     def __init__(self, name, func):
#         self.name = name
#         self.func = func

#     def __call__(self, *args):
#         return self.func(*args)

#     def __repr__(self):
#         return f"{self.name}"

#     def __str__(self):
#         return f"{self.name}"


# class Number:
#     def __init__(self, value):
#         self.value = value

#     def __repr__(self):
#         return f"{self.value}"

#     def __str__(self):
#         return f"{self.value}"


# class String:
#     def __init__(self, value):
#         self.value = value

#     def __repr__(self):
#         return f"{self.value}"

#     def __str__(self):
#         return f"{self.value}"


# class Array:
#     def __init__(self, value):
#         self.value = value

#     def __repr__(self):
#         return f"{self.value}"

#     def __str__(self):
#         return f"{self.value}"

#     def __getitem__(self, item):
#         return self.value[item]


# class Tuple:
#     def __init__(self, value):
#         self.value = value

#     def __repr__(self):
#         return f"{self.value}"

#     def __str__(self):
#         return f"{self.value}"

#     def __getitem__(self, item):
#         return self.value[item]


# class BlockStack:
#     def __init__(self):
#         self.stack = []

#     def __repr__(self):
#         return f"{self.stack}"

#     def __str__(self):
#         return f"{self.stack}"

#     def push(self, item):
#         self.stack.append(item)

#     def pop(self):
#         return self.stack.pop()

#     def peek(self):
#         return self.stack[-1]


stack_data = deque
# stack_data = list


class VoidType:
    """
    Sentinel value to indicate a function has no return value.
    Used to distinguish void functions from functions that explicitly return None.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self):
        return "VOID"

    def __bool__(self):
        return False


# Singleton instance
VOID = VoidType()


class String(str):
    def __init__(self, value: str):
        self.value = str(value)

    def __str__(self):
        return self.value

    def __add__(self, other: str) -> str:
        return self.value + other

    def __radd__(self, other: str) -> str:
        return other + self.value

    def startswith(self, value: str) -> bool:
        return self.value.startswith(value)

    def endswith(self, value: str) -> bool:
        return self.value.endswith(value)


class UndefinedSymbol(str):
    """Represents an undefined variable symbol.

    This type is used for identifiers that are not yet defined.
    When pushed to the stack, they remain as UndefinedSymbol.
    If an operation tries to use them (e.g., arithmetic), an error is raised.
    They can be consumed by 'set', 'defun', 'defmacro', 'do', 'dolist' as symbol names.
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"UndefinedSymbol({self.name!r})"


if __name__ == "__main__":
    s = String("hello")
    assert isinstance(s, str) is True
    assert isinstance(s, String) is True
    assert issubclass(String, str) is True

    s = "world"
    assert isinstance(s, str) is True
    assert isinstance(s, String) is False

    s1 = String("hello")
    s2 = String("world")
    s3 = s1 + s2
    print(s3)
    assert isinstance(s3, str) is True


--- stacker/stacker/syntax/__init__.py ---


--- stacker/stacker/syntax/parser.py ---
from __future__ import annotations

import ast
from functools import lru_cache
from typing import Any, List

# Import lexer components from the separate lexer module
from stacker.syntax.lexer import (
    Identifier,
    ListNode,
    Token,
    TokenType,
    TupleNode,
    UnifiedLexer,
    lex_string,
)

__transpose_symbol__ = "^T"


class Parser:
    """DEPRECATED: This parser includes tuple support which was removed in v1.9.0.

    Unified parser that handles both simple and complex parsing.
    Note: LPAREN now creates code blocks, not tuples.
    """

    def __init__(self, text: str) -> None:
        self.lexer = UnifiedLexer(text)
        self.tokens = iter(self.lexer.get_tokens())
        self.current_token = None
        self.next_token()

    def next_token(self) -> None:
        """Get the next token"""
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self) -> Union[ListNode, TupleNode]:
        """Parse input into appropriate node structure"""
        if self.current_token is None:
            return ListNode([])
        return self.parse_structure()

    def parse_structure(self) -> Union[ListNode, TupleNode]:
        """Parse a list or tuple structure"""
        elements = []

        if self.current_token.type == TokenType.LBRACKET:
            closing_type = TokenType.RBRACKET
            node_class = ListNode
        elif self.current_token.type == TokenType.LPAREN:
            closing_type = TokenType.RPAREN
            node_class = TupleNode
        else:
            raise SyntaxError(
                f"Expected LBRACKET or LPAREN, got {self.current_token.type}"
            )

        self.next_token()  # consume opening bracket/paren

        while self.current_token and self.current_token.type != closing_type:
            elements.append(self._parse_element())

        if self.current_token is None:
            raise SyntaxError(f"Expected {closing_type}, got EOF")

        self.next_token()  # consume closing bracket/paren

        if ";" in elements:
            return node_class(self._split_by_semicolon(elements, node_class))
        return node_class(elements)

    def _parse_element(self) -> Any:
        """Parse a single element within a structure"""
        if self.current_token is None:
            raise SyntaxError("Unexpected EOF while parsing element")

        if self.current_token.type in (TokenType.LBRACKET, TokenType.LPAREN):
            return self.parse_structure()

        token = self.current_token
        self.next_token()

        if token.type == TokenType.BRACED_CONTENT:
            return {"braced_content": token.value}
        elif token.type == TokenType.COMPLEX_NUMBER:
            return ast.literal_eval(token.value)
        elif token.type == TokenType.NUMBER:
            return ast.literal_eval(token.value)
        elif token.type == TokenType.STRING:
            return ast.literal_eval(token.value)
        elif token.type == TokenType.IDENTIFIER:
            return Identifier(token.value)
        elif token.type == TokenType.SEMICOLON:
            return ";"
        else:
            raise SyntaxError(f"Unexpected token {token}")

    def _split_by_semicolon(
        self, elements: List[Any], node_class: type[Union[ListNode, TupleNode]]
    ) -> List[Any]:
        """Split elements by semicolon into subnodes"""
        result = []
        current = []

        for item in elements:
            if item == ";":
                if current:
                    result.append(self._wrap_node(current, node_class))
                    current = []
            else:
                current.append(item)

        if current:
            result.append(self._wrap_node(current, node_class))

        return result

    def _wrap_node(
        self, elements: List[Any], node_class: type[Union[ListNode, TupleNode]]
    ) -> Any:
        """Wrap elements into appropriate node type"""
        if len(elements) == 1 and isinstance(elements[0], (ListNode, TupleNode)):
            return elements[0]
        return node_class(elements)


class Formatter:
    """Formats parsed structures back into string representation"""

    @staticmethod
    def format_structure(
        obj: Union[ListNode, TupleNode, int, float, complex, str, Identifier, dict],
    ) -> str:
        """Format any parsed structure back to string"""
        if isinstance(obj, ListNode):
            return f"[{','.join(Formatter.format_structure(item) for item in obj.elements)}]"
        elif isinstance(obj, TupleNode):
            return f"({','.join(Formatter.format_structure(item) for item in obj.elements)})"
        elif isinstance(obj, dict) and "braced_content" in obj:
            return f'"{obj["braced_content"].strip()}"'
        elif isinstance(obj, Identifier):
            return f"'{obj.name}'"
        elif isinstance(obj, str):
            return f"'\"{obj}\"'"
        elif isinstance(obj, complex):
            return str(obj)
        return str(obj)


def convert_custom_array_to_proper_list(input_str: str) -> str:
    """Convert custom array notation to proper list notation"""
    parser = Parser(input_str)
    parsed = parser.parse()

    # Flatten singleton structures
    while (
        isinstance(parsed, (ListNode, TupleNode))
        and len(parsed.elements) == 1
        and isinstance(parsed.elements[0], (ListNode, TupleNode))
    ):
        parsed = parsed.elements[0]

    return Formatter.format_structure(parsed)


@lru_cache(maxsize=512)
def _parse_expression_cached(expression: str) -> tuple[str, ...]:
    """Cached version of parse_expression that returns a tuple."""
    ignore_tokens = ['"""', "'''"]
    lexer = UnifiedLexer(expression)
    tokens = []

    for token in lexer.tokenize():
        if token in ignore_tokens:
            continue
        elif token.startswith("#"):
            return tuple(tokens)
        elif any(token.startswith(c) for c in "[({'\""):
            tokens.append(token)
        else:
            tokens.append(token)
    return tuple(tokens)


def parse_expression(expression: str) -> list[str]:
    """Parse expression into tokens while preserving structure"""
    # Use cached version and convert back to list
    return list(_parse_expression_cached(expression))


def evaluate_token_or_return_str(token: str) -> Any:
    if is_block(token):
        return token
    try:
        return ast.literal_eval(token)
    except (ValueError, SyntaxError):
        return token


def starts_with_char(expression: str, char: str) -> bool:
    try:
        return expression.strip().startswith(char)
    except Exception:
        return False


def remove_start_end_quotes(expression: str) -> str:
    if expression.startswith("'") and expression.endswith("'"):
        return expression[1:-1]
    if expression.startswith('"') and expression.endswith('"'):
        return expression[1:-1]
    return expression


def is_balanced(expression: str, open_char: str, close_char: str) -> bool:
    return expression.count(open_char) == expression.count(close_char)


def is_single(expression: str, open_char: str, close_char: str) -> bool:
    return (
        is_balanced(expression, open_char, close_char)
        and expression.count(open_char) == 1
        and expression.count(close_char) == 1
    )


def is_array(expression: str) -> bool:
    return starts_with_char(expression, "[")


def is_tuple(expression: str) -> bool:
    """DEPRECATED: Tuples removed in v1.9.0. Use is_code_block() instead.

    This function now checks for parenthesized code blocks, not tuples.
    """
    return starts_with_char(expression, "(")


def is_brace(expression: str) -> bool:
    return starts_with_char(expression, "{")


def is_array_balanced(expression: str) -> bool:
    return is_balanced(expression, "[", "]")


def is_tuple_balanced(expression: str) -> bool:
    """DEPRECATED: Tuples removed in v1.9.0. Use is_brace_balanced() instead.

    This function checks if parentheses are balanced (for code blocks).
    """
    return is_balanced(expression, "(", ")")


def is_brace_balanced(expression: str) -> bool:
    """Check if both {} and () code block delimiters are balanced."""
    return is_balanced(expression, "{", "}") and is_balanced(expression, "(", ")")


def is_single_array(expression: str) -> bool:
    return is_single(expression, "[", "]")


def is_single_tuple(expression: str) -> bool:
    """DEPRECATED: Tuples removed in v1.9.0.

    This function checks for single-level parenthesized code blocks.
    """
    return is_single(expression, "(", ")")


def is_single_brace(expression: str) -> bool:
    return is_single(expression, "{", "}")


def is_block(expression: str) -> bool:
    """Check if expression is a code block with {} delimiters.

    Note: For checking both {} and () code blocks, use is_code_block() instead.
    This function is kept for backward compatibility.
    """
    if not isinstance(expression, str):
        return False
    return expression.count("{") == expression.count("}") > 0


def is_code_block(expression: str) -> bool:
    """Check if expression is a code block (either {} or ()).

    Code blocks can be delimited by either curly braces {} or parentheses ().
    Both notations are functionally identical and create StackerCore substack objects.

    Args:
        expression: String to check

    Returns:
        True if expression has balanced braces or parentheses (non-empty), False otherwise

    Examples:
        >>> is_code_block("{1 2 +}")
        True
        >>> is_code_block("(1 2 +)")
        True
        >>> is_code_block("[1 2 3]")
        False
    """
    if not isinstance(expression, str):
        return False
    # Fast path: check first and last characters before counting
    if len(expression) < 2:
        return False
    first_char = expression[0]
    last_char = expression[-1]
    if first_char == "{" and last_char == "}":
        return expression.count("{") == expression.count("}")
    elif first_char == "(" and last_char == ")":
        return expression.count("(") == expression.count(")")
    return False


def is_string(expression: str) -> bool:
    if not isinstance(expression, str):
        return False
    return (expression.startswith("'") and expression.endswith("'")) or (
        expression.startswith('"') and expression.endswith('"')
    )


def is_list(expression: str) -> bool:
    if not isinstance(expression, str):
        return False
    return expression.startswith("[") and expression.endswith("]")


def is_symbol(expression: str) -> bool:
    """Check if expression is a valid symbol (e.g., $name, $my_var).

    Valid symbols:
    - Start with exactly one $
    - Followed by at least one character
    - Do not contain $ elsewhere

    Examples:
        $name -> True
        $x -> True
        $ -> False (no name after $)
        $$x -> False (multiple $ at start)
        $name$ -> False ($ at end)
    """
    if not isinstance(expression, str):
        return False
    if len(expression) < 2:  # At least "$x"
        return False
    if not expression.startswith("$"):
        return False
    if "$" in expression[1:]:  # No $ after the first character
        return False
    return True


def is_label_symbol(expression: str) -> bool:
    return expression.endswith(":") and not expression.startswith(":")


def is_transpose_command(expression: str) -> bool:
    return expression == __transpose_symbol__


def is_contains_transpose_command(expression: str) -> bool:
    return (
        len(expression) > len(__transpose_symbol__)
        and expression[-len(__transpose_symbol__) :] == __transpose_symbol__
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()


--- stacker/stacker/syntax/test_parser.py ---
import unittest

from stacker.syntax.parser import (
    evaluate_token_or_return_str,
    starts_with_char,
    remove_start_end_quotes,
    is_balanced,
    is_single,
    is_array,
    is_tuple,
    is_brace,
    is_array_balanced,
    is_tuple_balanced,
    is_brace_balanced,
    is_single_array,
    is_single_tuple,
    is_single_brace,
    is_block,
    is_string,
    is_list,
    is_symbol,
    is_label_symbol,
    is_transpose_command,
    is_contains_transpose_command,
    convert_custom_array_to_proper_list,
    parse_expression,
    lex_string,
)


class TestParser(unittest.TestCase):
    def test_evaluate_token_or_return_str(self):
        self.assertEqual(evaluate_token_or_return_str("123"), 123)
        self.assertEqual(evaluate_token_or_return_str("123.45"), 123.45)
        self.assertEqual(evaluate_token_or_return_str("'string'"), "string")
        self.assertEqual(evaluate_token_or_return_str("{block}"), "{block}")
        self.assertEqual(evaluate_token_or_return_str("invalid"), "invalid")

    def test_starts_with_char(self):
        self.assertTrue(starts_with_char("[1, 2, 3]", "["))
        self.assertFalse(starts_with_char("(1, 2, 3)", "["))

    def test_remove_start_end_quotes(self):
        self.assertEqual(remove_start_end_quotes("'string'"), "string")
        self.assertEqual(remove_start_end_quotes('"string"'), "string")
        self.assertEqual(remove_start_end_quotes("no_quotes"), "no_quotes")

    def test_is_balanced(self):
        self.assertTrue(is_balanced("[1, 2, 3]", "[", "]"))
        self.assertFalse(is_balanced("[1, 2, 3", "[", "]"))

    def test_is_single(self):
        self.assertTrue(is_single("[1, 2, 3]", "[", "]"))
        self.assertFalse(is_single("[1, 2, 3][4, 5, 6]", "[", "]"))

    def test_is_array(self):
        self.assertTrue(is_array("[1, 2, 3]"))
        self.assertFalse(is_array("(1, 2, 3)"))

    def test_is_tuple(self):
        # DEPRECATED: is_tuple() now checks for parenthesized code blocks, not tuples
        # Tuples were removed in v1.9.0
        self.assertTrue(is_tuple("(1, 2, 3)"))
        self.assertFalse(is_tuple("[1, 2, 3]"))

    def test_is_brace(self):
        self.assertTrue(is_brace("{1, 2, 3}"))
        self.assertFalse(is_brace("[1, 2, 3]"))

    def test_is_array_balanced(self):
        self.assertTrue(is_array_balanced("[1, 2, 3]"))
        self.assertFalse(is_array_balanced("[1, 2, 3"))

    def test_is_tuple_balanced(self):
        # DEPRECATED: is_tuple_balanced() now checks parentheses balance for code blocks
        # Tuples were removed in v1.9.0
        self.assertTrue(is_tuple_balanced("(1, 2, 3)"))
        self.assertFalse(is_tuple_balanced("(1, 2, 3"))

    def test_is_brace_balanced(self):
        self.assertTrue(is_brace_balanced("{1, 2, 3}"))
        self.assertFalse(is_brace_balanced("{1, 2, 3"))

    def test_is_single_array(self):
        self.assertTrue(is_single_array("[1, 2, 3]"))
        self.assertFalse(is_single_array("[1, 2, 3][4, 5, 6]"))

    def test_is_single_tuple(self):
        self.assertTrue(is_single_tuple("(1, 2, 3)"))
        self.assertFalse(is_single_tuple("(1, 2, 3)(4, 5, 6)"))

    def test_is_single_brace(self):
        self.assertTrue(is_single_brace("{1, 2, 3}"))
        self.assertFalse(is_single_brace("{1, 2, 3}{4, 5, 6}"))

    def test_is_block(self):
        self.assertTrue(is_block("{block}"))
        self.assertFalse(is_block("not_a_block"))

    def test_is_string(self):
        self.assertTrue(is_string("'string'"))
        self.assertTrue(is_string('"string"'))
        self.assertFalse(is_string("not_a_string"))

    def test_is_list(self):
        self.assertTrue(is_list("[1, 2, 3]"))
        self.assertFalse(is_list("(1, 2, 3)"))

    def test_is_symbol(self):
        self.assertTrue(is_symbol("$symbol"))
        self.assertFalse(is_symbol("symbol$"))

    def test_is_label_symbol(self):
        self.assertTrue(is_label_symbol("label:"))
        self.assertFalse(is_label_symbol(":label"))

    def test_is_transpose_command(self):
        self.assertTrue(is_transpose_command("^T"))
        self.assertFalse(is_transpose_command("not_transpose"))

    def test_is_contains_transpose_command(self):
        self.assertTrue(is_contains_transpose_command("matrix^T"))
        self.assertFalse(is_contains_transpose_command("matrix"))

    # ------------------------------------ #
    # convert_custom_array_to_proper_list  #
    # ------------------------------------ #
    def test_convert_custom_array_to_proper_list(self):
        self.assertEqual(
            convert_custom_array_to_proper_list("[1 2 3; 4 5 6]"), "[[1,2,3],[4,5,6]]"
        )
        self.assertEqual(convert_custom_array_to_proper_list("[1 2 3]"), "[1,2,3]")
        self.assertEqual(
            convert_custom_array_to_proper_list("[1 2 3; 4 5 6]"), "[[1,2,3],[4,5,6]]"
        )
        self.assertEqual(
            convert_custom_array_to_proper_list("['a' 'b' 'c']"),
            """['"a"','"b"','"c"']""",
        )
        self.assertEqual(
            convert_custom_array_to_proper_list("[a b c]"), "['a','b','c']"
        )
        self.assertEqual(
            convert_custom_array_to_proper_list("[1 'b' 3; 'd' 5 'f']"),
            "[[1,'\"b\"',3],['\"d\"',5,'\"f\"']]",
        )
        self.assertEqual(
            convert_custom_array_to_proper_list("[a 'b' c]"), "['a','\"b\"','c']"
        )
        self.assertEqual(convert_custom_array_to_proper_list("(1 2 3)"), "(1,2,3)")
        self.assertEqual(
            convert_custom_array_to_proper_list("(1 2 3; 4 5 6)"), "((1,2,3),(4,5,6))"
        )
        self.assertEqual(
            convert_custom_array_to_proper_list("((1 2; 3 4); (5 6; 7 8))"),
            "(((1,2),(3,4)),((5,6),(7,8)))",
        )
        self.assertEqual(
            convert_custom_array_to_proper_list("[1 2 3; (4 5 6; 7 8 9)]"),
            "[[1,2,3],((4,5,6),(7,8,9))]",
        )
        self.assertEqual(
            convert_custom_array_to_proper_list("[1 2.5 3.5]"), "[1,2.5,3.5]"
        )
        self.assertEqual(
            convert_custom_array_to_proper_list("[-1 -2 -3]"), "[-1,-2,-3]"
        )
        self.assertEqual(
            convert_custom_array_to_proper_list("[1 2+3j 4+5j]"), "[1,(2+3j),(4+5j)]"
        )
        self.assertEqual(
            convert_custom_array_to_proper_list("(1 2.5 3.5)"), "(1,2.5,3.5)"
        )
        self.assertEqual(
            convert_custom_array_to_proper_list("(-1 -2 -3)"), "(-1,-2,-3)"
        )
        self.assertEqual(
            convert_custom_array_to_proper_list("(1 2+3j 4+5j)"), "(1,(2+3j),(4+5j))"
        )

    def test_convert_custom_array_to_proper_list_3d_array(self):
        self.assertEqual(
            convert_custom_array_to_proper_list(
                "[[[1 2 3; 4 5 6]; [7 8 9; 10 11 12]]; [[13 14 15; 16 17 18]; [19 20 21; 22 23 24]]]"
            ),
            "[[[[1,2,3],[4,5,6]],[[7,8,9],[10,11,12]]],[[[13,14,15],[16,17,18]],[[19,20,21],[22,23,24]]]]",
        )

    def test_parse_expression(self):
        self.assertEqual(parse_expression("[1 2 3] 4 5 a"), ["[1 2 3]", "4", "5", "a"])
        self.assertEqual(parse_expression("(1)"), ["(1)"])

    def test_block_1(self):
        self.assertEqual(
            parse_expression("{x}{x 1 +}lambda"), ["{x}", "{x 1 +}", "lambda"]
        )

    def test_block_2(self):
        self.assertEqual(parse_expression("3{1 +}"), ["3", "{1 +}"])


class TestLexer(unittest.TestCase):
    def test_basic_tokens(self):
        self.assertEqual(lex_string("a b c"), ["a", "b", "c"])
        self.assertEqual(lex_string("a [b c]"), ["a", "[b c]"])
        self.assertEqual(lex_string("a (b c)"), ["a", "(b c)"])
        self.assertEqual(lex_string("a {b c}"), ["a", "{b c}"])
        self.assertEqual(lex_string("a 'b c'"), ["a", "'b c'"])
        self.assertEqual(lex_string('a "b c"'), ["a", '"b c"'])

    def test_mixed_tokens(self):
        self.assertEqual(lex_string("a 'b c' d"), ["a", "'b c'", "d"])
        self.assertEqual(lex_string('a "b c" d'), ["a", '"b c"', "d"])
        self.assertEqual(lex_string("a 'b c' d 'e f'"), ["a", "'b c'", "d", "'e f'"])
        self.assertEqual(lex_string("a {b c} {d e}"), ["a", "{b c}", "{d e}"])
        self.assertEqual(
            lex_string("a {b c {d e}} {f h}"), ["a", "{b c {d e}}", "{f h}"]
        )

    def test_single_brackets(self):
        self.assertEqual(lex_string("[1]"), ["[1]"])
        self.assertEqual(lex_string("(1)"), ["(1)"])

    def test_complex_expression(self):
        expr = "1 2 3 [4 5 6] 7 8 (9 10 11) a1 b1 c1 {1 2 +} '1+1' eval"
        exprs = [
            "1",
            "2",
            "3",
            "[4 5 6]",
            "7",
            "8",
            "(9 10 11)",
            "a1",
            "b1",
            "c1",
            "{1 2 +}",
            "'1+1'",
            "eval",
        ]
        self.assertEqual(lex_string(expr), exprs)


if __name__ == "__main__":
    unittest.main()


--- stacker/stacker/syntax/lexer.py ---
from __future__ import annotations

import re
import warnings
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Iterator, List


class TokenType(Enum):
    BRACED_CONTENT = auto()
    COMPLEX_NUMBER = auto()
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LPAREN = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    OPERATOR = auto()
    SPACE = auto()
    COMMA = auto()
    OTHER = auto()


@dataclass
class Token:
    """Represents a single token."""

    type: TokenType
    value: str

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


@dataclass
class Identifier:
    """Represents an identifier."""

    name: str

    def __repr__(self) -> str:
        return f"Identifier({self.name})"


@dataclass
class ListNode:
    """Represents a list node."""

    elements: List[Any]

    def __repr__(self) -> str:
        return f"ListNode({self.elements})"


@dataclass
class TupleNode:
    """DEPRECATED: Tuples removed in v1.9.0.

    This class is kept for backward compatibility but should not be used.
    Parentheses () now create code blocks, not tuples.
    """

    elements: List[Any]

    def __repr__(self) -> str:
        return f"TupleNode({self.elements})"


class TokenPattern:
    """Token patterns for lexical analysis"""

    PATTERNS = [
        (TokenType.BRACED_CONTENT, r"\{[^}]*\}"),
        (
            TokenType.COMPLEX_NUMBER,
            r"[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?[+-](\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?[jJ]",
        ),
        (TokenType.NUMBER, r"[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?[jJ]?"),
        (TokenType.STRING, r"('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")"),
        (TokenType.IDENTIFIER, r"[A-Za-z_][A-Za-z0-9_]*"),
        (TokenType.LBRACKET, r"\["),
        (TokenType.RBRACKET, r"\]"),
        (TokenType.LPAREN, r"\("),
        (TokenType.RPAREN, r"\)"),
        (TokenType.SEMICOLON, r";"),
        (TokenType.OPERATOR, r"[+\-]"),
        (TokenType.SPACE, r"\s+"),
        (TokenType.COMMA, r","),
        (TokenType.OTHER, r"."),
    ]


class UnifiedLexer:
    """Unified lexical analyzer that handles both simple and complex tokenization"""

    # Class-level cache for regex patterns (optimization)
    _cached_token_re = None

    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.delimiter_mapping = {"[": "]", "(": ")", "{": "}", "'": "'", '"': '"'}
        self._setup_regex()

    def _setup_regex(self) -> None:
        """Setup regex patterns for tokenization (cached at class level)"""
        if UnifiedLexer._cached_token_re is None:
            tok_regex = "|".join(
                f"(?P<{pattern[0].name}>{pattern[1]})"
                for pattern in TokenPattern.PATTERNS
            )
            UnifiedLexer._cached_token_re = re.compile(tok_regex)
        self.token_re = UnifiedLexer._cached_token_re

    def tokenize(self) -> list[str]:
        """Tokenize input preserving nested structures"""
        tokens = []
        current_token = ""
        bracket_stack = []
        escaped = False  # Track if previous char was backslash

        for char in self.text:
            # Check if we're inside a string literal
            in_string = bracket_stack and bracket_stack[-1] in ['"', "'"]

            # Handle escaped characters in strings
            if in_string and escaped:
                current_token += char
                escaped = False
                continue

            # Check for escape character in strings
            if in_string and char == '\\':
                current_token += char
                escaped = True
                continue

            if char in self.delimiter_mapping:
                if current_token and current_token.strip().isdigit():
                    tokens.append(current_token)
                    current_token = ""

                if bracket_stack and self.delimiter_mapping[bracket_stack[-1]] == char:
                    current_token += char
                    bracket_stack.pop()
                    if not bracket_stack:
                        tokens.append(current_token)
                        current_token = ""
                # If we're inside a string, only the matching quote closes it
                # All other characters (including other quotes) are literal
                elif in_string:
                    current_token += char
                else:
                    bracket_stack.append(char)
                    current_token += char
            elif bracket_stack:
                current_token += char
                if char == self.delimiter_mapping[bracket_stack[-1]]:
                    bracket_stack.pop()
                    if not bracket_stack:
                        tokens.append(current_token)
                        current_token = ""
            elif char.isspace():
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
            else:
                current_token += char

        if current_token:
            tokens.append(current_token)

        return tokens

    def get_tokens(self) -> Iterator[Token]:
        """Get tokens with type information"""
        pos = 0
        while pos < len(self.text):
            match = self.token_re.match(self.text, pos)
            if match is None:
                break

            kind = TokenType[match.lastgroup]  # type: ignore
            value = match.group()
            if kind != TokenType.SPACE:
                yield Token(kind, value)

            pos = match.end()

        if pos != len(self.text):
            raise SyntaxError(
                f"Unexpected character {self.text[pos]!r} at position {pos}"
            )


def lex_string(s: str) -> list:
    """
    Deprecated: Use UnifiedLexer(s).tokenize() instead.

    Tokenize a string into a list of tokens.
    """
    warnings.warn(
        "lex_string() is deprecated. Use UnifiedLexer(s).tokenize() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return UnifiedLexer(s).tokenize()


--- stacker/stacker/util/disp.py ---
from __future__ import annotations


from stacker.util import colored
from stacker.engine.data_type import String

from typing import Any


class CustomPrinter:
    def __init__(self, value: Any, color: str):
        self.value = value
        self.color = color

    def __str__(self):
        return colored(str(self.value), self.color)

    def __repr__(self):
        return str(self.value)


class CustomIntPrinter(CustomPrinter):
    def __init__(self, value: int, color: str):
        self.value = value
        self.color = color


class CustomFloatPrinter(CustomPrinter):
    def __init__(self, value: float, color: str):
        self.value = value
        self.color = color


class CustromComplexPrinter(CustomPrinter):
    def __init__(self, value: complex, color: str):
        self.value = value
        self.color = color


class CustomStrPrinter(CustomPrinter):
    def __init__(self, value: str, color: str):
        self.value = value
        self.color = color


class CustomBoolPrinter(CustomPrinter):
    def __init__(self, value: bool, color: str):
        self.value = value
        self.color = color

    def __str__(self):
        return colored(str(self.value).lower(), self.color)

    def __repr__(self):
        return str(self.value).lower()


class CustomListPrinter(CustomPrinter):
    def __init__(self, value: list, color: str):
        # self.value = [custom_print(item) for item in value]
        self.value = value
        self.color = color

    def __str__(self):
        _temp = list(map(custom_print, self.value))
        return colored(str(_temp).replace(",", ""), self.color)

    def __repr__(self):
        return str(self.value).replace(",", "")


# REMOVED: CustomTuplePrinter - () now creates code blocks, not tuples
# Tuples are no longer a primary data type in Stacker


class OperatorPrinter(CustomPrinter):
    def __init__(self, value: Any, color: str):
        self.value = value
        self.color = color

    def __str__(self):
        return colored(str(self.value), self.color)

    def __repr__(self):
        return str(self.value)


class CustomBlockPrinter(CustomPrinter):
    def __init__(self, value: Any, color: str):
        self.value = value
        self.color = color

    def __str__(self):
        return colored(str(self.value), self.color)

    def __repr__(self):
        return str(self.value)


class CustomStringPrinter(CustomPrinter):
    def __init__(self, value: Any, color: str):
        self.value = value
        self.color = color

    def __str__(self):
        return colored("'" + str(self.value) + "'", self.color)

    def __repr__(self):
        return self.__str__()


class CutomCallablePrinter(CustomPrinter):
    def __init__(self, value: Any, color: str):
        self.value = value
        self.color = color

    def __str__(self):
        return colored(str(self.value), self.color)

    def __repr__(self):
        return str(self.value)


color_map = {
    "int": "default",
    "float": "default",
    "complex": "default",
    "str": "default",  # variable symbol
    "String": "lightgreen",
    "bool": "lightblue",
    "list": "red",
    # "tuple": "red",  # REMOVED: Tuples no longer supported
    "block": "cyan",
    "callable": "yellow",
}


def custom_print(value: Any) -> CustomPrinter:
    from stacker.stacker import Stacker

    if isinstance(value, bool):
        return CustomBoolPrinter(value, color_map["bool"])
    if isinstance(value, int):
        return CustomIntPrinter(value, color_map["int"])
    if isinstance(value, float):
        return CustomFloatPrinter(value, color_map["float"])
    if isinstance(value, complex):
        return CustromComplexPrinter(value, color_map["complex"])
    if isinstance(value, String):
        return CustomStringPrinter(value, color_map["String"])
    if isinstance(value, str):
        return CustomStrPrinter(value, color_map["str"])
    if isinstance(value, list):
        return CustomListPrinter(value, color_map["list"])
    # REMOVED: tuple handling - () now creates code blocks
    if isinstance(value, Stacker):
        return CustomBlockPrinter(value, color_map["block"])
    if callable(value):
        return CutomCallablePrinter(value, color_map["callable"])
    return value


def disp_colored(stack_list: list) -> str:
    stack_str = colored("[", "yellow")
    for item in stack_list:
        stack_str += str(custom_print(item))
        stack_str += " "
    stack_str = stack_str[0:-1]
    stack_str += colored("]", "yellow")
    return stack_str


def disp_default(stack_list: list) -> str:
    return f"{stack_list}".replace(",", "")


def disp_stack(stack_list, colored: bool = False):
    if colored:
        print(disp_colored(stack_list))
    else:
        print(disp_default(stack_list))


--- stacker/stacker/util/__init__.py ---
from stacker.util.color import COLORS, colored

__all__ = ["COLORS", "colored"]


--- stacker/stacker/util/color.py ---
from __future__ import annotations

COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "lightgray": "\033[37m",
    "default": "\033[39m",
    "darkgray": "\033[90m",
    "lightred": "\033[91m",
    "lightgreen": "\033[92m",
    "lightyellow": "\033[93m",
    "lightblue": "\033[94m",
    "lightmagenta": "\033[95m",
    "lightcyan": "\033[96m",
    "white": "\033[97m",
    "reset": "\033[0m",
}


def colored(text: str, color: str = "default") -> str:
    """A context manager for setting and resetting the terminal color.
    Args:
        color (str, optional): The desired text color. Defaults to "default".
    Returns:
        None
    """
    ctext = COLORS[color] + text + COLORS["reset"]
    return ctext


--- stacker/stacker/plugins/whos.py ---
# from stacker.stacker import Stacker


# def whos(stacker):
#     labels = ["Name", "Size", "Class"]
#     names = stacker.variables.keys()
#     for label in labels:
#         print(f"{label}\t", end="")
#     print("")
#     for name in names:
#         _value = stacker.variables[name]
#         _type = str(type(_value))
#         _size = 1
#         if isinstance(_value, list) or isinstance(_value, tuple):
#             try:
#                 # n dim (n > 1)
#                 _size = [len(v) for v in _value]
#             except TypeError:
#                 # 1 dim
#                 _size = len(_value)
#         print(f"{name}\t{_size}\t{_type}")


# def setup(stacker: Stacker):
#     stacker.register_plugin(
#         operator_name="whos",
#         operator_func=whos,
#         push_result_to_stack=False,
#         pass_core=True,
#         desc="Show the variables in the stacker",
#     )


def setup(stacker):
    pass


--- stacker/stacker/plugins/__init__.py ---


--- stacker/stacker/plugins/matrix.py ---
# from __future__ import annotations

# import numpy as np

# from stacker.stacker import Stacker

# description = "Matrix operations plugin for Stacker"


# """
# A + B (matrix addition)
#     A = [1, 2; 3, 4]
#     B = [5, 6; 7, 8]
#     A + B
#     ans
#         6   8
#         10  12

# a + b (scalar addition)
#     a = 1
#     b = 2
#     c = a + b
#     c = 3
# """


# def _add(a, b):
#     if type(a) is str or type(b) is str:
#         return a + b
#     return (np.array(a) + np.array(b)).tolist()


# """
# A - B (matrix subtraction)
#     A = [1, 2; 3, 4]
#     B = [5, 6; 7, 8]
#     A - B
#     ans =
#         -4  -4
#         -4  -4

# a - b (scalar subtraction)
#     a = 1
#     b = 2
#     c = a - b
#     c = -1
# """


# def _sub(a, b):
#     return (np.array(a) - np.array(b)).tolist()


# """
# A * B (matrix multiplication)
#     A = [1, 2; 3, 4]
#     B = [5, 6; 7, 8]
#     C = A * B
#     C =
#         19  22
#         43  50

# a * b (scalar multiplication)
#     a = 1
#     b = 2
#     c = a * b
#     c = 2
# """


# def _mul(a, b):
#     if np.array(a).shape == () and np.array(b).shape == ():
#         return a * b
#     else:
#         return np.dot(a, b).tolist()

#     # _a = np.array(a)
#     # _b = np.array(b)
#     # if _a.shape == () and _b.shape == ():
#     #     return a * b
#     # else:
#     #     if _a[-1] != _b[0]:
#     #         raise ValueError(
#     #             f"Matrix dimensions must agree. Got {_a.shape} and {_b.shape}."
#     #         )
#     #     return np.dot(_a, _b).tolist()


# """
# A .* B (element-wise multiplication)
#     A = [1, 2; 3, 4]
#     B = [5, 6; 7, 8]
#     C = A .* B
#     C =
#         5   12
#         21  32
# """


# def _adamul(a, b):
#     return np.multiply(a, b).tolist()


# """
# A / B (matrix division)
#     A = [1, 2; 3, 4]
#     B = [5, 6; 7, 8]
#     A / B
#     ans =
#         3.0 -2.0
#         2.0 -1.0
#     # A * inv(B)
# """


# def _div(a, b):
#     if (
#         np.array(a).shape == () and np.array(b).shape == ()
#     ):  # scalar and scalar division
#         return a / b
#     else:
#         return np.dot(a, np.linalg.inv(b)).tolist()


# """
# A ./ B (element-wise division)
#     A = [1, 2; 3, 4]
#     B = [5, 6; 7, 8]
#     A ./ B
#     ans =
#         0.2000 0.3333
#         0.4286 0.5000

# """


# def _elemdiv(a, b):
#     return np.divide(a, b).tolist()


# """
# A \ B (left division, solve for x in Ax = B)
#     A = [1, 2; 3, 4]
#     B = [5, 6; 7, 8]
#     A \ B
#     ans =
#         -3.0000  -4.0000
#         4.0000   5.0000

# """


# def _leftdiv(a, b):
#     return np.linalg.solve(a, b).tolist()


# """
# A .\ B (element-wise left division)
# """


# def _elemldiv(a, b):
#     return np.divide(b, a).tolist()


# """
# A ^ B (matrix power)
#     A = [1, 2; 3, 4]
#     B = 2
#     A ^ B
#     ans =
#         7  10
#         15 22
# """


# def _pow(a, b):
#     if np.array(a).shape == () and np.array(b).shape == ():
#         return _elempow(a, b)
#     return np.linalg.matrix_power(a, b).tolist()


# """
# A .^ B (element-wise power)
#     A = [1, 2; 3, 4]
#     B = [5, 6; 7, 8]
#     A .^ B
#     ans =
#         1 64
#         2187 65536
# """


# def _elempow(a, b):
#     return np.power(a, b).tolist()


# """
# A | B (element logical OR)
#     A = [0 1 0 2[]
#     B = [0 0 3 -2]
#     A | B
#     ans =
#         False True False True
# """


# def _logical_or(a, b):
#     return np.logical_or(a, b).tolist()


# """
# A & B (element logical AND)
#     A = [0 1 0 2]
#     B = [0 0 3 -2]
#     A & B
#     ans =
#         False False False True
# """


# def _logical_and(a, b):
#     return np.logical_and(a, b).tolist()


# """
# ~A (logical NOT)
#     A = [0 1 0 2]
#     ~A
#     ans =
#         True False True False
# """


# def _logical_not(a):
#     return np.logical_not(a).tolist()


# """
# A xor B (logical XOR)
#     A = [0 1 0 2]

# """


# def _logical_xor(a, b):
#     return np.logical_xor(a, b).tolist()


# """
# A == B (equality)
#     A = [1, 2; 3, 4]
#     B = [1, 2; 3, 4]
#     ans =
#         True True
#         True True
# """


# def _eq(a, b):
#     return (np.array(a) == np.array(b)).tolist()


# """
# A
# """

# """
# A' (transpose)
#     A = [1, 2; 3, 4]
#     B = A'
#     B =
#         1 3
#         2 4
# """


# def _transpose(a):
#     return np.transpose(a).tolist()


# """
# A.' (conjugate transpose)
#     A = [1, 2; 3, 4]
#     B = A.'
#     B =
#         1 3
#         2 4
# """


# def _ctranspose(a):
#     return np.conjugate(np.transpose(a)).tolist()


# """
# inv(A) (inverse)
#     A = [1, 2; 3, 4]
#     B = inv(A)
#     B =
#         -2  1
#         1.5 -0.5
# """


# def _inv(a):
#     return np.linalg.inv(a).tolist()


# """
# det(A) (determinant)
#     A = [1, 2; 3, 4]
#     B = det(A)
#     B = -2
# """


# def _det(a):
#     return np.linalg.det(np.array(a)).tolist()


# """
# dot(A, B) (dot product)
# """


# def _dot(a, b):
#     _a = np.array(a)
#     _b = np.array(b)
#     if _a[-1] != _b[0]:
#         raise ValueError(
#             f"Matrix dimensions must agree. Got {_a.shape} and {_b.shape}."
#         )
#     return np.dot(_a, _b).tolist()


# """
# rank(A) (rank)
#     A = [1, 2; 3, 4]
#     B = rank(A)
#     B = 2

# """


# def _rank(a):
#     return int(np.linalg.matrix_rank(np.array(a)))


# """
# trace(A) (trace)
#     A = [1, 2; 3, 4]
#     B = trace(A)
#     B = 5
# """


# def _trace(a):
#     return int(np.trace(np.array(a)))


# """
# ones(m, n) (ones)
#     A = ones(2, 3)
#     A =
#         1 1 1
#         1 1 1
# """


# def _ones(*args):
#     return np.ones(args).tolist()


# """
# zeros(m, n) (zeros)
#     A = zeros(2, 3)
#     A =
#         0 0 0
#         0 0 0
# """


# def _zeros(*args):
#     return np.zeros(args).tolist()


# """
# diag(A) (diagonal)
#     A = [1, 2; 3, 4]
#     B = diag(A)
#     B =
#         1
#         4
# """


# def _diag(*args):
#     return np.diag(*args).tolist()


# # def ndim(a) -> int:
# #     if not isinstance(a, np.ndarray):
# #         return np.ndim(a)
# #     else:
# #         return np.ndim(np.array(a))


# # def size(a) -> int:
# #     if not isinstance(a, np.ndarray):
# #         return np.size(a)
# #     else:
# #         return np.size(np.array(a))


# # def shape(a) -> tuple:
# #     if not isinstance(a, np.ndarray):
# #         return np.shape(a)
# #     else:
# #         return np.shape(np.array(a))


# def _all(a) -> bool:
#     return bool(np.all(a))


# def _any(a) -> bool:
#     return bool(np.any(a))


# def setup(stacker: Stacker):
#     stacker.register_plugin("+", _add, desc="Matrix Addition")
#     stacker.register_plugin("-", _sub, desc="Matrix Subtraction")
#     stacker.register_plugin("*", _mul, desc="Matrix Multiplication")
#     stacker.register_plugin(".*", _adamul, desc="Element-wise Multiplication")
#     stacker.register_plugin("/", _div, desc="Matrix Division")
#     stacker.register_plugin("./", _elemdiv, desc="Element-wise Division")
#     stacker.register_plugin("\\", _leftdiv, desc="Left Division")  # \
#     stacker.register_plugin(".\\", _elemldiv, desc="Element-wise Left Division")  # .\
#     stacker.register_plugin("^", _pow, desc="Matrix Power")
#     stacker.register_plugin(".^", _elempow, desc="Element-wise Power")
#     stacker.register_plugin("or", _logical_or, desc="Logical OR")
#     stacker.register_plugin("and", _logical_and, desc="Logical AND")
#     stacker.register_plugin("not", _logical_not, desc="Logical NOT")
#     stacker.register_plugin("xor", _logical_xor, desc="Logical XOR")
#     stacker.register_plugin("==", _eq, desc="Equality")
#     stacker.register_plugin("'", _transpose, desc="Transpose")
#     stacker.register_plugin("dot", _dot, desc="Dot Product")
#     stacker.register_plugin("inv", _inv, desc="Inverse")
#     stacker.register_plugin("det", _det, desc="Determinant")
#     stacker.register_plugin("rank", _rank, desc="Rank")
#     stacker.register_plugin("trace", _trace, desc="Trace")
#     stacker.register_plugin("ones", _ones, desc="Ones")
#     stacker.register_plugin("zeros", _zeros, desc="Zeros")
#     stacker.register_plugin("diag", _diag, desc="Diagonal")
#     # stacker.register_plugin("ndim", ndim, desc="Number of Dimensions")
#     # stacker.register_plugin("size", size, desc="Size")
#     # stacker.register_plugin("shape", shape, desc="Shape")
#     stacker.register_plugin("all", _all, desc="All")
#     stacker.register_plugin("any", _any, desc="Any")


def setup(stacker):
    pass


--- stacker/stacker/runtime/__init__.py ---
from stacker.runtime.exec_modes import (
    CommandLineMode,
    ExecutionMode,
    ReplMode,
    ScriptMode,
    create_error_message,
)

__all__ = [
    "ExecutionMode",
    "ReplMode",
    "ScriptMode",
    "CommandLineMode",
    "create_error_message",
]


--- stacker/stacker/runtime/exec_modes/commandline_mode.py ---
from __future__ import annotations

import sys

from stacker.runtime.exec_modes.error import create_error_message
from stacker.runtime.exec_modes.execution_mode import ExecutionMode


class CommandLineMode(ExecutionMode):
    def run(self, expression: str):
        try:
            self.rpn_calculator.eval(expression)
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
            trace = self.rpn_calculator.get_trace_copy()
            if len(trace) == 0:
                sys.exit(1)
            if len(trace) > 4:
                error_trace = trace[-4:]
            else:
                error_trace = trace
            print(create_error_message(error_trace))
            sys.exit(1)


--- stacker/stacker/runtime/exec_modes/script_mode.py ---
from __future__ import annotations

import sys
from pathlib import Path

from stacker.error import ScriptReadError, StackerError
from stacker.runtime.exec_modes.execution_mode import ExecutionMode
from stacker.include.stk_file_read import readtxt
from stacker.lib.config import script_extension_name
from stacker.stacker import Stacker
from stacker.error_formatter import ErrorFormatter
# from stacker.util.color import colored
# from stacker.exec_modes.error import create_error_message


class ScriptMode(ExecutionMode):
    def __init__(self, rpn_calculator: Stacker):
        self.col_count = 0
        super().__init__(rpn_calculator)

    def run(self, file_path: str):
        try:
            path = Path(file_path)
            if not path.is_file() or not path.suffix == script_extension_name:
                raise ScriptReadError(
                    f"Invalid file path or file type. Please provide a valid '{script_extension_name}' file."
                )

            # Use the parent class's execute_stacker_dotfile which handles multi-line properly
            self.execute_stacker_dotfile(path)
        except Exception as e:
            # Format error using Clang-style formatter
            error_type = type(e).__name__
            message = str(e)

            # Get line number and source line from tracked information
            line_number = self.rpn_calculator.current_line
            source_line = None
            if line_number is not None and line_number in self.rpn_calculator.source_lines:
                source_line = self.rpn_calculator.source_lines[line_number]

            column = None  # We don't track column yet

            # Generate hint based on error type
            hint = self._get_error_hint(e)

            # Format the error
            formatted_error = ErrorFormatter.format_error(
                filename=str(Path(file_path).resolve()),
                line_number=line_number,
                column=column,
                error_type=error_type,
                message=message,
                source_line=source_line,
                hint=hint
            )

            print(formatted_error, file=sys.stderr)
            sys.exit(1)

    def _get_error_hint(self, error: Exception) -> str | None:
        """Generate helpful hint based on error type."""
        error_type = type(error).__name__
        message = str(error)

        # Undefined variable/symbol errors
        if "UndefinedSymbol" in error_type or "UndefinedVariable" in error_type:
            # Extract variable name from message
            if "`" in message:
                var_name = message.split("`")[1]
                return f"Define '{var_name}' before using it: '0 {var_name} ='"

        # Stack underflow errors
        elif "StackUnderflow" in error_type:
            # Message already contains operator and arg count info
            return "Check that you have enough values on the stack before calling this operator"
        elif "IndexError" in error_type and "pop from an empty deque" in message:
            return "Stack underflow: Not enough elements on the stack for this operation"

        # Division errors
        elif "ZeroDivisionError" in error_type:
            return "Cannot divide by zero. Check your divisor value"

        # Type errors
        elif "TypeError" in error_type:
            if "concatenate str" in message or "can only concatenate str" in message:
                return "Cannot mix string and number types. Use 'str' to convert numbers to strings"
            elif "unsupported operand type" in message:
                if "+" in message:
                    return "The '+' operator requires compatible types (both numbers or both strings)"
                elif "*" in message:
                    return "Multiplication requires numeric types or string * int"
                elif "-" in message or "/" in message:
                    return "Arithmetic operators require numeric types"
                return "Check that the operator receives compatible argument types"
            elif "not subscriptable" in message:
                return "Cannot index into this type. Use '[]' for lists or 'nth' for sequence access"
            elif "not callable" in message:
                return "This value cannot be called as a function"

        # Key errors (variable not found)
        elif "KeyError" in error_type:
            # Extract key name from message
            key = message.strip("'\"")
            return f"Variable '{key}' is not defined. Define it first: '0 {key} ='"

        # Syntax errors
        elif "SyntaxError" in error_type or "StackerSyntaxError" in error_type:
            if "bracket" in message.lower() or "paren" in message.lower():
                return "Check for matching brackets: {} for code blocks, [] for lists"
            elif "quote" in message.lower():
                return "Check for matching quotes in strings"

        # File errors
        elif "FileNotFoundError" in error_type:
            return "File not found. Check the file path is correct"
        elif "PermissionError" in error_type:
            return "Permission denied. Check file permissions"

        # Attribute errors
        elif "AttributeError" in error_type:
            return "This value does not have the requested attribute or method"

        return None

        # with path.open('r') as script_file:
        #     expression = ''
        #     for line in script_file:
        #         line = line.strip()
        #         if line.startswith('#') or not line:  # ignore comments and empty lines
        #             continue
        #         expression += line + ' '
        #         if self._is_balanced(expression):
        #             if expression[-2:] in {";]", ";)"}:
        #                 closer = expression[-1]
        #                 expression = expression[:-2] + closer
        #             self.rpn_calculator.process_expression(expression)
        #             expression = ''


--- stacker/stacker/runtime/exec_modes/__init__.py ---
from stacker.runtime.exec_modes.commandline_mode import CommandLineMode
from stacker.runtime.exec_modes.error import create_error_message
from stacker.runtime.exec_modes.execution_mode import ExecutionMode
from stacker.runtime.exec_modes.repl_mode import ReplMode
from stacker.runtime.exec_modes.script_mode import ScriptMode

__all__ = [
    "ExecutionMode",
    "ReplMode",
    "ScriptMode",
    "CommandLineMode",
    "create_error_message",
]


--- stacker/stacker/runtime/exec_modes/execution_mode.py ---
from __future__ import annotations

from pathlib import Path

from stacker.include.stk_file_read import readtxt
from stacker.stacker import Stacker

# Import parser utility functions (not lexer components)
# Lexer components (TokenType, UnifiedLexer, etc.) are in stacker.syntax.lexer
from stacker.syntax.parser import (
    is_array_balanced,
    is_brace_balanced,
    # is_tuple_balanced,  # REMOVED: () now creates code blocks, use is_brace_balanced
    remove_start_end_quotes,
)

# from stacker.syntax.parser import is_string
from stacker.util.disp import disp_stack

# def simple_format(arr):
#     """
#     Format the specified list as a simple string.
#     Example:
#         [[2.999999999999992, -1.9999999999999942], [1.9999999999999947, -0.9999999999999964]]
#         -> [[3.0000, -2.0000], [2.0000, -1.0000]]
#     """

#     def format_number(x):
#         if isinstance(x, int):
#             return str(x)
#         if isinstance(x, str):
#             return x
#         if isinstance(x, bool):
#             return str(x).lower()
#         return f"{x:.4f}"

#     def format_recursive(item):
#         if not isinstance(item, list):
#             return format_number(item)
#         elif isinstance(item, list):
#             return [format_recursive(subitem) for subitem in item]
#         elif isinstance(item, tuple):
#             return tuple(format_recursive(subitem) for subitem in item)
#         else:
#             return item
#         # else:
#         #     formatted_items = [format_recursive(subitem) for subitem in item]
#         #     return "[" + " ".join(formatted_items) + "]"

#     return format_recursive(arr)


class ExecutionMode:
    def __init__(self, rpn_calculator: Stacker):
        self.rpn_calculator = rpn_calculator
        self.color_print = True
        self.debug = False

    def debug_mode(self):
        self.debug = True

    def get_multiline_input(self, prompt="") -> str:
        lines = []
        while True:
            line = input(prompt)
            if line.endswith("\\"):
                line = line[:-1]  # remove trailing backslash
                lines.append(line)
                prompt = ""  # no prompt for subsequent lines
            else:
                lines.append(line)
                break
        return "\n".join(lines)

    def run(self):
        raise NotImplementedError("Subclasses must implement the 'run' method")

    def disp(self) -> None:
        """Print the current stack to the console."""
        _stack = self.rpn_calculator.get_stack_copy_as_list()
        disp_stack(_stack, colored=self.color_print)
        # if self.color_print is True:
        #     stack_str = disp_colored(_stack)
        #     print(stack_str)
        # else:
        #     print(f"{_stack}".replace(",", ""))

    def disp_all_variables(self) -> None:
        variables = self.rpn_calculator.get_variables_copy()
        for key in variables.keys():
            print(f"{key} = {variables[key]}")

    def disp_ans(self) -> None:
        _stack = self.rpn_calculator.get_stack_copy_as_list()
        if len(_stack) == 0:
            return
        print(f"{_stack[-1]}")

    def execute_stacker_dotfile(self, filename: str | Path) -> None:
        """Import a stacker script and return the stacker object."""
        path = Path(remove_start_end_quotes(str(filename)))
        code = readtxt(path)
        expression = ""
        lines = code.splitlines()

        # Set source file and store all source lines for error reporting
        self.rpn_calculator.current_file = str(path.resolve())
        for line_num, line_text in enumerate(lines, start=1):
            self.rpn_calculator.source_lines[line_num] = line_text

        i = 0
        expression_start_line = None  # Track which line the expression started on

        while i < len(lines):
            line = lines[i].strip()
            line_number = i + 1  # 1-indexed line numbers

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                i += 1
                continue

            # Track the first line of the expression
            if not expression.strip():
                expression_start_line = line_number

            # Remove inline comments from the line before adding to expression
            # Find # that is not inside a string
            clean_line = line
            if '#' in line:
                in_string = False
                quote_char = None
                for j, char in enumerate(line):
                    if char in ('"', "'") and (j == 0 or line[j-1] != '\\'):
                        if not in_string:
                            in_string = True
                            quote_char = char
                        elif char == quote_char:
                            in_string = False
                            quote_char = None
                    elif char == '#' and not in_string:
                        clean_line = line[:j].rstrip()
                        break

            expression += clean_line + " "

            if self._is_balanced(expression):
                if self._is_complete_expression(expression):
                    if expression[-2:] in {";]", ";)"}:
                        closer = expression[-1]
                        expression = expression[:-2] + closer
                    # Set current line before processing expression
                    self.rpn_calculator.current_line = expression_start_line
                    self.rpn_calculator.process_expression(expression)
                    expression = ""
                    expression_start_line = None

            i += 1

    def _is_balanced(self, expression: str) -> bool:
        # Inline comments are already removed before calling this method
        return (
            is_array_balanced(expression)
            # REMOVED: is_tuple_balanced - () now handled by is_brace_balanced
            and is_brace_balanced(expression)  # Handles both {} and () code blocks
            and (expression.count('"""') % 2 == 0)
            and (expression.count("'''") % 2 == 0)
        )

    def _is_complete_expression(self, expression: str) -> bool:
        """Check if the expression is complete and ready to execute.

        Some commands like 'do', 'dolist', 'times' require arguments that may
        span multiple lines. We need to check if all required arguments are present.
        """
        from stacker.syntax.parser import parse_expression, is_code_block

        try:
            tokens = parse_expression(expression.strip())
            if not tokens:
                return True

            # Commands that require a code block and symbol/values before execution
            block_consuming_commands = {"do", "dolist", "times"}

            # Check if the last token is a block-consuming command
            last_token = tokens[-1] if tokens else None
            if last_token not in block_consuming_commands:
                return True

            # For 'do': expects start_value end_value symbol {body} do
            if last_token == "do":
                if len(tokens) < 5:
                    return False
                # Check if there's a code block before 'do'
                return is_code_block(str(tokens[-2]))

            # For 'dolist': expects list symbol {body} dolist
            if last_token == "dolist":
                if len(tokens) < 4:
                    return False
                # Check if there's a code block before 'dolist'
                return is_code_block(str(tokens[-2]))

            # For 'times': expects {body} n times
            if last_token == "times":
                if len(tokens) < 3:
                    return False
                # Check if there's a code block two positions before 'times'
                return is_code_block(str(tokens[-3]))

            return True
        except Exception:
            # If parsing fails, assume it's incomplete
            return False


--- stacker/stacker/runtime/exec_modes/error.py ---
from __future__ import annotations

from stacker.util.color import colored


def create_error_message(error_tokens: list[str]):
    last_token = error_tokens[-1]
    expression = " ".join([str(token) for token in error_tokens])
    hilight = " " * (len(expression) - len(last_token)) + "^" * len(last_token)
    return colored(f"{expression}\n{hilight}", "red")


def create_error_message_from_str(code: str):
    return colored(code, "red")


--- stacker/stacker/runtime/exec_modes/repl_mode.py ---
from __future__ import annotations

import logging
import sys
import traceback

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from importlib.metadata import version
from stacker.runtime.exec_modes.error import create_error_message
from stacker.runtime.exec_modes.execution_mode import ExecutionMode
from stacker.lib import delete_history, disp_about, disp_help
from stacker.lib.config import history_file_path
from stacker.error_formatter import ErrorFormatter

# Import parser utility functions (not lexer components)
# Lexer components (TokenType, UnifiedLexer, etc.) are in stacker.syntax.lexer
from stacker.syntax.parser import (
    is_array,
    is_array_balanced,
    is_brace,
    is_brace_balanced,
    is_code_block,
    # is_tuple,  # REMOVED: Tuples no longer supported
    # is_tuple_balanced,  # REMOVED: Use is_brace_balanced for () blocks
)


class ReplMode(ExecutionMode):
    def __init__(self, rpn_calculator):
        super().__init__(rpn_calculator)
        # REPL-specific display settings
        self.disp_stack_mode = True
        self.disp_logo_mode = True
        self.disp_ans_mode = False
        # REPL-specific command list
        self.repl_commands = [
            "help",
            "about",
            "delete_history",
        ]
        # Initialize completer
        self.completer = WordCompleter(self.get_completer())

    def get_completer(self):
        """Get completion words for REPL prompt."""
        _reserved_word = list(self.repl_commands)
        _operator_key = list(self.rpn_calculator.get_all_keys_for_completer())
        _priority_operators_key = list(
            self.rpn_calculator.operator_manager.get_priority_keys()
        )
        _sfunctions_key = list(self.rpn_calculator.get_sfuntions_ref().keys())
        _variable_key = list(self.rpn_calculator.get_variables_ref().keys())
        _macro_key = list(self.rpn_calculator.get_macros_ref().keys())
        _reserved_word = list(
            set(
                _reserved_word
                + _operator_key
                + _priority_operators_key
                + _sfunctions_key
                + _variable_key
                + _macro_key
            )
        )
        return _reserved_word

    def update_completer(self):
        self.completer = WordCompleter(self.get_completer())

    def get_input(self, prompt_text: str, multiline: bool):
        try:
            return prompt(
                prompt_text,
                history=FileHistory(history_file_path),
                completer=self.completer,
                multiline=multiline,
            )
        except EOFError:
            print("\nSee you!")
            sys.exit()

    def get_version(self) -> str:
        return version("pystacker")

    # REPL Command Handlers
    def _cmd_help(self) -> None:
        """Handle 'help' command."""
        disp_help()
        print("")
        print("Supported operators and functions:")
        regular_operator_descriptions = {}
        regular_operator_descriptions.update(
            self.rpn_calculator.operator_manager.get_regular_descriptions()
        )
        regular_operator_descriptions.update(
            self.rpn_calculator.operator_manager.get_priority_descriptions()
        )
        for (
            operator_name,
            operator_descriptions,
        ) in regular_operator_descriptions.items():
            print(f"  {operator_name}:\t{operator_descriptions}")
        print("")
        print("Stack operators:")
        for (
            operator_name,
            operator_descriptions,
        ) in self.rpn_calculator.operator_manager.get_stack_descriptions().items():
            print(f"  {operator_name}:\t{operator_descriptions}")
        print("")
        print("Settings operators:")
        for (
            operator_name,
            operator_descriptions,
        ) in self.rpn_calculator.operator_manager.get_settings_descriptions().items():
            print(f"  {operator_name}:\t{operator_descriptions}")
        print("")
        print("System operators:")
        for (
            operator_name,
            operator_descriptions,
        ) in self.rpn_calculator.operator_manager.get_system_descriptions().items():
            print(f"  {operator_name}:\t{operator_descriptions}")
        print("")
        print("Plugin commands:")
        for (
            plugin_name,
            plugin_descriptions,
        ) in self.rpn_calculator.plugin_descriptions.items():
            print(f"  {plugin_name}: {plugin_descriptions}")

    def _cmd_about(self) -> None:
        """Handle 'about' command."""
        disp_about()

    def _cmd_delete_history(self) -> None:
        """Handle 'delete_history' command."""
        delete_history()

    def _get_error_hint(self, error: Exception) -> str | None:
        """Generate helpful hint based on error type."""
        error_type = type(error).__name__
        message = str(error)

        if "UndefinedSymbol" in error_type:
            # Extract variable name from message
            if "`" in message:
                var_name = message.split("`")[1]
                return f"Define '{var_name}' before using it: '0 {var_name} ='"
        elif "IndexError" in error_type and "pop from an empty deque" in message:
            return "Stack underflow: Not enough elements on the stack for this operation"
        elif "ZeroDivisionError" in error_type:
            return "Cannot divide by zero"
        elif "TypeError" in error_type:
            if "concatenate str" in message:
                return "Cannot mix string and number types. Convert one to match the other"

        return None

    def _handle_repl_command(self, expression: str) -> bool:
        """
        Handle REPL-specific commands.
        Returns True if command was handled, False otherwise.
        """
        expr_lower = expression.lower()

        # Simple command handlers
        if expr_lower == "help":
            self._cmd_help()
            return True
        if expr_lower == "about":
            self._cmd_about()
            return True
        if expr_lower == "delete_history":
            self._cmd_delete_history()
            return True

        # Display mode commands
        if expr_lower == "enable_disp_stack":
            self.disp_stack_mode = True
            return True
        if expr_lower == "disable_disp_stack":
            self.disp_stack_mode = False
            return True
        if expr_lower == "enable_disp_logo":
            self.disp_logo_mode = True
            return True
        if expr_lower == "disable_disp_logo":
            self.disp_logo_mode = False
            return True
        if expr_lower == "enable_disp_ans":
            self.disp_ans_mode = True
            return True
        if expr_lower == "disable_disp_ans":
            self.disp_ans_mode = False
            return True

        return False

    def run(self):
        stacker_version = self.get_version()
        print(f"Stacker {stacker_version} on {sys.platform}")
        print('Type "help" to get more information.')

        line_count = 0
        while True:
            try:
                expression = self.get_input(f"stacker:{line_count}> ", multiline=False)
                if expression[-2:] in {";]", ";)"}:
                    closer = expression[-1]
                    expression = expression[:-2] + closer

                if is_brace(expression):
                    # """
                    #     # Brace
                    #     stacker:0> {1
                    #                 3
                    #                 +}
                    #     {1 3 +}
                    # """
                    while not is_brace_balanced(expression):
                        prompt_text = (
                            " " * (len(f"stacker:{line_count}> ") - len("> ")) + "> "
                        )
                        next_line = self.get_input(prompt_text, multiline=False)
                        expression += " " + next_line
                        if next_line in {"}"}:
                            if is_brace_balanced(expression):
                                break

                if is_array(expression) or is_code_block(expression):
                    # """
                    #     # List
                    #     stacker:0> [1 2 3
                    #                 3 4 5]
                    #     [1 2 3; 3 4 5]
                    #
                    #     # Code Block
                    #     stacker:0> (1 2 3
                    #                 3 4 5)
                    #     (1 2 3; 3 4 5)
                    # """
                    while not is_array_balanced(expression) or not is_brace_balanced(
                        expression
                    ):
                        prompt_text = (
                            " " * (len(f"stacker:{line_count}> ") - len("> ")) + "> "
                        )
                        next_line = self.get_input(prompt_text, multiline=False)
                        if next_line.lower() == ("end"):
                            break
                        if next_line in {"]", ")"}:
                            expression += next_line
                            if is_array_balanced(expression) or is_brace_balanced(
                                expression
                            ):
                                if expression[-2:] in {";]", ";)"}:
                                    closer = expression[-1]
                                    expression = expression[:-2] + closer
                                break
                        if next_line[-2:] in {";]", ";)"}:
                            closer = next_line[-1]
                            next_line = next_line[:-2] + closer
                        if not expression.endswith(";"):
                            expression += "; " + next_line
                        else:
                            expression += " " + next_line

                # # Process to continue until the input starting with double quotation or single quotation is closed
                # while (
                #     (expression.startswith('"""') and expression.count('"""') % 2 != 0) or
                #     (expression.startswith("'''") and expression.count("'''") % 2 != 0)
                # ):
                #     """
                #         stacker:0> '''
                #         stacker:0> This is a multi-line
                #         stacker:0> input example.
                #         stacker:0> '''
                #         ['\nThis is a multi-line\ninput example.\n']
                #     """
                #     prompt_text = " " * (len(f"stacker:{line_count}> ") - len("> ")) + "> "
                #     next_line = self.get_input(prompt_text, multiline=False)
                #     expression += "\n" + next_line

                logging.debug("input expression: %s", expression)

                # Handle REPL-specific commands
                if self._handle_repl_command(expression):
                    continue

                # Process as normal RPN expression
                self.rpn_calculator.process_expression(expression)
                if self.disp_ans_mode is True:
                    self.disp_ans()
                if self.disp_stack_mode is True:
                    self.disp()
                # else:
                #     if self.rpn_calculator.get_stack_length() > 0:
                #         print(self.rpn_calculator.get_stack_copy_as_list()[-1])
                #     else:
                #         print(self.rpn_calculator.get_stack_copy_as_list())
                self.rpn_calculator.clear_trace()

            except EOFError:
                print("\nSee you!")
                break

            except Exception as e:
                # Format error using Clang-style formatter
                error_type = type(e).__name__
                message = str(e)

                # Generate hint based on error type
                hint = self._get_error_hint(e)

                # Format the error (REPL mode doesn't have file/line info)
                formatted_error = ErrorFormatter.format_error(
                    filename=None,  # REPL has no file
                    line_number=None,  # REPL has no line numbers
                    column=None,
                    error_type=error_type,
                    message=message,
                    source_line=None,
                    hint=hint
                )

                print(formatted_error, file=sys.stderr)

                # Show trace only in debug mode
                if self.debug:
                    trace = self.rpn_calculator.get_trace_copy()
                    if len(trace) > 0:
                        if len(trace) > 4:
                            error_trace = trace[-4:]
                        else:
                            error_trace = trace
                        print(create_error_message(error_trace), file=sys.stderr)
                    traceback.print_exc()

                self.rpn_calculator.clear_trace()
            # self.update_completer()
            line_count = self.rpn_calculator.get_stack_length()


