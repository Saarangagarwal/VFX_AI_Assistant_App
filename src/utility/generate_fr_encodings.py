from face_recognition_operations import fr_encoding_gen, fr_dump_encodings

def generate_fr_encodings():
    # call the generate encoding function for face recognition algorithm
    knownNames, knownEncodings = fr_encoding_gen()

    # save encodings to the file system
    fr_dump_encodings(knownEncodings, knownNames)


def main():
    generate_fr_encodings()


if __name__ == '__main__':
    main()
