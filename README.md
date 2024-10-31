# Givtu-Test-Mgmt 🚀

## Purpose of the Repository 🎯
The repository provides the tooling for testing our backend environments
<br><br>

---




## Promo Keys  🔑 
This module contains tools for managing, testing, and automating key allocation. It includes command-line utilities to display, allocate, and export key allocation data in various formats.

### Features
- **Show Key Status**: Check active and total keys for users, with paginated viewing options.
- **Allocate Keys**: Distribute keys based on fixed quantity or percentage increase methods.
- **Export Key Data**: Generate a CSV report of key allocation data for specific evaluation dates.


### CLI Usage

### Commands

#### Show Key Status
Displays the active and total keys for each user on a given date, with pagination support.

**Usage:**

```commandline
python3 -m promo_keys.promo_keys_cli show-keys --date "YYYY-MM-DD HH:MM" --env <environment> --page-size <size>
```

**Arguments:**

- `--date` (required): The evaluation date and time in the format YYYY-MM-DD HH:MM:SS. Determines which keys are considered active.
- `--env` (optional): Specifies the database environment (dev, staging, production). Default is staging.
- `--page-size` (optional): Sets the number of results per page. Default is 10.

**Example:**

```bash
python3 -m promo_keys.promo_keys_cli show-keys --date "2024-10-29 10:00:00" --env dev --page-size 20
```


#### Allocate Keys
Allocates a specified quantity of keys to users. The allocation can be based on a fixed quantity or a percentage increase of current keys.

**Usage:**

```commandline
python3 -m promo_keys.promo_keys_cli  allocate-keys --method <method> --value <value> --eval_date "YYYY-MM-DD HH:SS:MM" --active_date "YYYY-MM-DD HH:SS:MM" --env <environment> --filename <filename>
```

**Arguments:**

- `--method` (required): The allocation method. Choose `fixed_qty` for a fixed quantity or `percentage_increase` to allocate based on a percentage of current keys.
- `--value` (required): The amount of keys to allocate. For `fixed_qty`, it’s the number of keys. For `percentage_increase`, it’s the percentage.
- `--eval_date` (required): The evaluation date in YYYY-MM-DD format, used to determine active keys.
- `--active_date` (required): The date in YYYY-MM-DD format from which the allocated keys become active.
- `--only_active_keys` (optional): If specified, calculates the percentage increase based on only active keys.
- `--env` (optional): Specifies the database environment (dev, staging, production). Default is dev.
- `--filename` (required): Base filename for before and after allocation export files.

**Example:**

```bash
python3 -m promo_keys.promo_keys_cli  allocate-keys --method 'fixed_qty' --value 1 --eval_date "2024-10-27 10:00:00" --active_date "2024-10-29 10:00:00" --env dev --filename test-run
```


#### Export Key Table
Exports key allocation data for each user on a specified date to a CSV file.

**Usage:**


```commandline
python3 -m promo_keys.promo_keys_cli export-key-table --date "YYYY-MM-DD HH:MM" --env <environment> --output <output>
```


**Arguments:**

- `--date` (required): The evaluation date and time in YYYY-MM-DD HH:MM:SS format.
- `--env` (optional): Specifies the database environment (dev, staging, production). Default is staging.
- `--output` (optional): Specifies the filename for the output CSV. Default is key_allocation.csv.

**Example:**



```bash
python3 -m promo_keys.promo_keys_cli export-key-table --date "2024-10-29 10:00:00" --env dev --output
```

<br><br>

---


## Cron Jobs ⏰

---

## Create Games 🎮

---

## Testing 🧪

- To run test ```pytest <test_file>```
- E.g. ```pytest test_submit_order.py``` will run all tests in the ```test_submit_order.py``` file. 
- Refer to ```https://docs.pytest.org/en/stable/``` to understand how ```pytest``` works.

### TODO

- [ ] Move all testing apis into a test controller on php side
- [ ] Use a password to ensure only givtu users can access api
- [ ] Do not make any of these testing features accessible during production

