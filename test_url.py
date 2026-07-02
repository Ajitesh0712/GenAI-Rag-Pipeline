from services.indexer import index_url

count = index_url(
    "https://en.wikipedia.org/wiki/Grand_Theft_Auto"
)

print(count)