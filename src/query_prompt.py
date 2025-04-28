# flake8: noqa
CUSTOM_QUERY_CHECKER = """
{query}
Double check the {dialect} query above for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins
 
If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.
Do not make assumptions or infer information that is not explicitly provided. Avoid speculative or fabricated logic.
NEVER alter user-provided names or personal values (e.g., FirstName, LastName). **Preserve exact spelling**, even if it appears incorrect. Do NOT make assumptions or corrections to these values. Use them in the SQL query **as-is**.
Handle possessive names correctly. Assume that possessive names like "Steve Roger's" refer to someone whose last name is "Roger".
Orders Table is the central table (all filtering happens here).
ServiceTeamId filtering is mandatory in every query.
Tables must be joined based on actual relationships (PK ↔ FK).
Always make sure the filtering condition 'ServiceTeamId in...' is present in the final query
Output the final SQL query only.
 
SQL Query: """