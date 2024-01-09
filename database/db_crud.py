# Holds all mongoDB read writes actions
from fastapi import HTTPException, status


async def add_single_document(collection, document):
    """adds asingle document to the mongoDB collection

    collection: the mongoDB collection to insert documnets into
    documents: a dictionary object representing the document to insert to a mongoDB collection
    """

    result = await collection.insert_one(document)
    return result


async def add_multiple_documents(collection, doc_array):
    """adds multiple documnets to the mongoDB collection

    collections: denotes the collection in mongoDB
    doc_array: an array of dictionaries to add to mongoDB collection
    """

    result = await collection.insert_many(doc_array)
    return result


async def fetch_all_documents(
    collection, collection_object, doc_filters=None
):
    """returns all documents on the mongoDB collection

    @collection: the mongoDB collection
    @collection_object: pydantic model,
    @doc_filters: a dictionary containing the filter conditions
    """

    if doc_filters:
        documents = collection.find(doc_filters)

    else:
        documents = collection.find()

    return [collection_object(**document) async for document in documents]


async def fetch_one(collection, **kwargs):
    """returns documents that match **kwargs parameter"""

    if not kwargs:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="no filter condition passed",
        )

    result = await collection.find_one(kwargs)
    return result


async def remove_one_document(collection, **kwargs):
    """deletes a document from mongoDB collection"""

    if not kwargs:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="no filter condition passed",
        )

    await collection.delete_one(kwargs)
    return True


async def remove_many_document(collection, doc_array):
    """removes document array from mongoDB collection"""

    await collection.delete_many(doc_array)
    return True
