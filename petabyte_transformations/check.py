from solution_0 import bad_blobs_list

if __name__ == "__main__":

    bad_blobs_before_cleaning = bad_blobs_list("./blobs")
    print("Bad blobs before cleaning: {0}".format(len(bad_blobs_before_cleaning)))
    for b in bad_blobs_before_cleaning:
        print(b)

    bad_blobs_after_cleaning_0 = bad_blobs_list("./clean_blobs_1")
    print("\n\nBad blobs after cleaning 0: {0}".format(len(bad_blobs_after_cleaning_0)))
    for b in bad_blobs_after_cleaning_0:
        print(b)

    bad_blobs_after_cleaning_1 = bad_blobs_list("./clean_blobs_2")
    print("\n\nBad blobs after cleaning 1: {0}".format(len(bad_blobs_after_cleaning_1)))
    for b in bad_blobs_after_cleaning_1:
        print(b)

    bad_blobs_after_cleaning_1_bytes = bad_blobs_list("./clean_blobs_2_bytes")
    print(
        "\n\nBad blobs after cleaning 1 bytes: {0}".format(
            len(bad_blobs_after_cleaning_1_bytes)
        )
    )
    for b in bad_blobs_after_cleaning_1_bytes:
        print(b)
