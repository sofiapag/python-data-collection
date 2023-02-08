GOAL: create a flexible schema for collecting data on farming practices users have performed on their fields over the last several years.

It is your task to:

- Define and implement a database schema that can store this configuration.
- Expose a REST API to create/delete these entities.
- Handle some validation of inputs where sensible.

User can:

- input year
- input tillage depth
- input crop type
- add comments
- any additional arbitrary fields and their limits

Assumptions:

- 1 Entry per year

Schema:
Let `?` signify optional fields.
Let `//` signify comments.

Features table {
id: int
name: string // ex. Fall Tillage
collectionMethod: string // ex. selector, textbox, date, number, slider
possibleValues?: [] string // ex. [ 'Reduced Tillage', 'Conventional Tillage' ]
minValue?: number
maxValue?: number
defaultValue?: string | number | date | boolean
info?: string // The text that shows up when you click on the `?` icon
}
// if feature is slider, require min/max values
// if feature is selector, require possible values

UserInputTable table {
id: int
features: [] int // list of featureId's
startYear: number
endYear: number
}

## Summarizing Thoughts

Having Features as their own table allows us to flexibly add any number and type of new features to a table. Those features are referenced by their ID's in the UserInputTable type, which is simply a collection of featureIds, and a year range.

I ran into some complications with not being able to store lists in the sqlite DB, so any lists would be stored as strings (meant to be parsed when used). Future improvement would be to allow, validate, and parse list/array inputs.

Additional future improvements would be to define a GET method for a single UserInputTable, which would resolve featureIds in `userInputTable.features` to the actual features, and the endpoint would return an object of the below form. This resolution of featureIds could also be done on the existing GET method (that gets all UserInputTables).

```
{
  id: 123,
  features: [
    {
      name: "Fall Tillage",
      collectionMethod: "selector",
      ...
    },
    ...
  ],
  startYear: 2020,
  endYear: 2023
}
```
