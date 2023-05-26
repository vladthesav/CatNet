CatPicEmbeddings (
    imgID int UNIQUE PRIMARY KEY NOT NULL,
    embeddingType varchar(255) NOT NULL,
    embedding VARCHAR(255) NOT NULL
);