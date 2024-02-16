from face_recognition_operations import fr_encoding_gen, fr_dump_encodings

def main():
    # call the generate encoding function for face recognition algorithm
    knownNames, knownEncodings = fr_encoding_gen()

    # save encodings to the file system
    fr_dump_encodings(knownEncodings, knownNames)

if __name__ == '__main__':
    main()
