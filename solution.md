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
I will make an assumption that they can be combined into 1 table like this:

| External Account ID    | Year              | Crop Type                                                     | Tilled? | Tillage Depth                                                        | Comments |
| ---------------------- | ----------------- | ------------------------------------------------------------- | ------- | -------------------------------------------------------------------- | -------- |
| Regex Validated String | Four digit number | Constrained Picklist (might be [corn, wheat, barley, hops...] | Bool    | Constrained Float ie must be `0 <= x < 10`, can be optionally filled | String   |

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
