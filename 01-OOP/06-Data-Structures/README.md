# Data Structures

In this exercise, we will cover the most useful built-in data structures.
Before diving into the code, take some time to read the following:

- [Lists](https://docs.python.org/3.8/tutorial/introduction.html#lists), called _array_ in other languages
- [More on lists](https://docs.python.org/3.8/tutorial/datastructures.html#more-on-lists)
- [List Comprehensions](https://docs.python.org/3.8/tutorial/datastructures.html#list-comprehensions)
- [Tuples](https://docs.python.org/3.8/tutorial/datastructures.html#tuples-and-sequences)
- [Dictionaries](https://docs.python.org/3.8/tutorial/datastructures.html#dictionaries), called _hash_ or _hashmap_ in other languages
- [Looping Techniques](https://docs.python.org/3.8/tutorial/datastructures.html#looping-techniques) with the `for` keyword

All read? Let's code!

## Getting Started

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 01-OOP/06-Data-Structures
code .
```

## Exercise

### Currencies

Let's build a currency converter in the `currencies.py` file. In this exercise, we will manipulate lists, dictionaries and tuples.

1. Create a new constant dictionary `RATES` at the top of `currencies.py`. Keys will be 6-letter strings like `"USDEUR"`, `"GBPEUR"`, `"CHFEUR"`, and values their rate stored as a simple Python [`float` number](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex). You can find this information on [Google](https://www.google.com/search?q=USDEUR)
1. Implement the `convert(amount, currency)` method. The first parameter is a **tuple** of two elements: a float and a currency (e.g. `(100, "USD")`). The second parameter is a `String`, the currency you want to convert the amount into.
1. To simplify, we will consider amounts as cents and _round_ result.
1. When called with an unknown rate (e.g. `"RMBEUR"`), the `convert` method should return `None`.

Run the tests with:

```bash
nosetests
```

You may notice some tests failing. Update your rates with the following values as results have been hard-coded in the tests:

- `USDEUR`: `0.85`
- `GBPEUR`: `1.13`
- `CHFEUR`: `0.86`

At last, check your style with:

```bash
pipenv run pylint currencies.py
```

## (Optional) Data Structures in PowerShell

PowerShell come with the following:

- [Arrays](https://docs.microsoft.com/powershell/module/microsoft.powershell.core/about/about_arrays) (equivalent of Python's `list`)
- [Hash Tables](https://docs.microsoft.com/powershell/module/microsoft.powershell.core/about/about_hash_tables) (equivalent of Python's `dict`)

Now try to implement a script which behaves like the following examples:

```bash
powershell -ExecutionPolicy bypass ./convertor.ps1
# => Amount is required.

powershell -ExecutionPolicy bypass ./convertor.ps1 -Amount 12.4
# => Destination currency is required.

powershell -ExecutionPolicy bypass ./convertor.ps1 -Amount 12.4 -Currency AAA
# => Sorry, currency AAA is not yet supported

powershell -ExecutionPolicy bypass ./convertor.ps1 -Amount 12.4 -Currency GBP
# => 12.4 EUR => 14.012 GBP
```

You may need to use [`Hashtable.ContainsKey(key)`](https://docs.microsoft.com/dotnet/api/system.collections.hashtable.containskey).

<details><summary markdown="span">View solution
</summary>

```powershell
param(
  [double]$Amount = $(throw "Amount is required."),
  [string]$Currency = $(throw "Destination currency is required.")
)

$rates = @{
  USDEUR = 0.85;
  GBPEUR = 1.13;
  CHFEUR = 0.86
}

$key = $Currency + "EUR"

if ($rates.ContainsKey($key)) {
  $result = ($Amount * $rates[$key])
  Write-Output "$Amount EUR => $result $Currency"
} else {
  Write-Error "Sorry, currency $Currency is not yet supported"
}
```

</details>
