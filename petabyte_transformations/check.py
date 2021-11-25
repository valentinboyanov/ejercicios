from solution_0 import bad_blobs_list

BLOBS_PATH = "./blobs"
CLEAN_BLOBS_PATH = "./clean_blobs_2"

if __name__ == "__main__":

    bad_blobs_before_cleaning = bad_blobs_list(BLOBS_PATH)
    print("Bad blobs before cleaning: {0}".format(len(bad_blobs_before_cleaning)))
    for b in bad_blobs_before_cleaning:
        print(b)

    bad_blobs_after_cleaning = bad_blobs_list(CLEAN_BLOBS_PATH)
    print("\n\nBad blobs after cleaning: {0}".format(len(bad_blobs_after_cleaning)))
    for b in bad_blobs_after_cleaning:
        print(b)
