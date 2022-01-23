# Face-Recognition-With-Postgresql
A demonstration of offloading image processing operations to an SQL server.

We are using Postgresql to store and process the image processing data such as Face Embeddings. To run this you must setup a Postgresql sever in your local machine or have network access to any machine with Postgresql.

I have used LFW(labeled faces in the wild) dataset from http://vis-www.cs.umass.edu/lfw/ for creating face embeddings database. Make sure to download the dataset and extract it in the same directory as this file.

