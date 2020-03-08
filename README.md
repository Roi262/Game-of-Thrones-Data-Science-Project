# Data-Science---Final-Project
csvs parsing:
    preprocess_files.py - script to clean kaggle files, 
    removes irrelevant information 
    srt-to-csv.py - script to transform srt file to a csv file format


data_manipulation:
    join_srt_and_scenes.py - join srt file with the scenes file: for every scene find the lines in that scene in the srt file
    text_parser.py - a python script that merges the speaker, lines csv with the dataset created in join_srt_and_scenes


part_1:
    Make sparse vectors.py - For the lines of the top d characters, stem and create feature vectors (one hot and additional features) and then write to file in a sparse form with the correct labels
    word_to_id.py - Creates the words map file - each word (unless it's a stopword) gets an ID number according to how frequent it is. This is used for the onehot vectors
    Predict_by_probability.py - A baseline model that "predicts" the speaker at random. The distribution is not uniform, it is weighted by the characters amount of lines spoken
    Knn.py - Applies the k-nearest-neighbors algorithm to the sparse feature vectors and plots the accuracy for different k values
    cnn.py - The cnn model for part 1


part_a_lstm:
    data_reder.py - read the data to numpy array
    split_data_and_labels.py - split the data and labels, and save them as numpy arrays
    lstm_nn.py - the lstm model for part 1


Part_2:
    lstm:
        clean_data.py - a python file with various functions that clean and remove
        irrelevent data from csv files
        configure.py - a configure file
        features.py - creates feature vectors for lines in the script
        lstm.py - handles lstm NN learner
        split_data_and_labels.py - split the data and labels, and save them as numpy arrays


Part_3:
    analysis.py - creates dialogues between pairs and analyzes their sentiment
    throughout the show


part4:
    part4.py - sentiment analysis of sentences that sain on characters


configure.py - a global configure file



