# Solution to the Problem:

## Two Tables

At the first glance, I tried to understand the relationship between these two tables.

> Typically, a table may look like this example:
>
> | Year              | Crop Type                                                     | Tillage Depth                                                        | Comments |
> | ----------------- | ------------------------------------------------------------- | -------------------------------------------------------------------- | -------- |
> | Four digit number | Constrained Picklist (might be [corn, wheat, barley, hops...] | Constrained Float ie must be `0 <= x < 10`, can be optionally filled | String   |
>
> However, due to the flexibility of our offering, this is not the only data we want to collect. We may want to collect something like:
>
> | Year              | Tilled? | External Account ID    | Tillage Depth                    |
> | ----------------- | ------- | ---------------------- | -------------------------------- |
> | Four digit number | Bool    | Regex Validated String | Slider Control mapped to a float |

They seemed to be similar and there is to be no obviously reason to split this crop "entity" into two tables.
There is no foreign key that would allow the joining of these two tables.
I will make an assumption that they can be combined into 1 table like this. Let's call it the `Crop` table.

| External Account ID    | Year              | Crop Type                                                     | Tilled? | Tillage Depth                                                        | Comments |
| ---------------------- | ----------------- | ------------------------------------------------------------- | ------- | -------------------------------------------------------------------- | -------- |
| Regex Validated String | Four digit number | Constrained Picklist (might be [corn, wheat, barley, hops...] | Bool    | Constrained Float ie must be `0 <= x < 10`, can be optionally filled | String   |

In this combined table, I will assume that the `External Account ID` is a foreign key of `User` id in code.
A user / farmer may plant multiple types of crops across many years. So, the relationship is 1-to-many between `User` and `Crop`.

## Get only the data you need

### GraphQL Approach

We can implement a solution for this requirement by using GraphQL. With GraphQL, the client specifies what fields are needed in a query then the server will return data for the specifies fields, nothing less and nothing more.

> By the same token, we may want some other, unique set of columns that are picked from both the examples. You need to design and implement a solution that would let you represent both examples and any combination/permuation of their constituent columns.

For example, a graphql query could look like this:

```graphql
{
    query ($userId: UserId) {
        cropsByUser(userId: $userId){
            userId
            year
            cropType
            tilled
            tillageDepth
            comments
        }
    }
}
```

With graphql variable like:

```json
{ "userId": 12345 }
```

The client is free to omit 1 or multiple fields in the graphql query and get back only the data of interest.
The output of this query will be an array of crops with specified fields pertaining to a certain user.

### REST Approach

REST API typically returns a fixed number of fields as define by an API contract, i.e. OpenAPI / Swagger docs.
It is possible to enable field selection in a REST API approach by accepting a query parameter called "fields".
The value for this "fields" parameter could be a comma-separated list.

The endpoint could look like this:

```
/crops/{user_id}?fields=user_id,year,crop_type
```

In the view/route/endpoint function, we can manipulate the SQL result to include only the selected fields.
The downside is that it breaks a consistent API contract and creates friction for system integration.
It is better for the REST API to return the full payload with all the fields to maintain a consistent API contract.
The downstream client who received the full payload can decide what fields to use and what to not use.

### Pagination

This is a topic of pagination. When an array is potentially unbounded from a database query, we should implement pagination to ensure the operation is not too taxing on the database, app server and also the front-end.

> Additionally, as per the screenshot, some configuration must be present to tell the UI how many years of data we wish to collect (hence how many rows to render).

There are several ways to implement pagination. For example with page_size and page_num:

```
/crops/{user_id}?page_size=10&page_num=3
```

page_size determines the number of items in a page while page_num can be used to iterate or traverse all the records.

Another option is to use limit and offset:

```
/crops/{user_id}?limit=10&offset=50
```

On the database level, it is typically limit and offset. It can be implemented as page_size and page_num for convenience to the user.

### SQL Migration

This is a topic of SQL migration.

> In the future we may want to collect other information too; these columns are not fixed.

Typically, adding new columns to a table or adding new fields to an API response is not a breaking change. Deleting columns, changing the type or nullability of the column could be a breaking changing.
