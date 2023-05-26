CREATE TABLE RedditCatPics (
    imgID int UNIQUE PRIMARY KEY NOT NULL,
    subReddit varchar(255),
    catBreed VARCHAR(255),
    postID varchar(255),
    redditImgID varchar(255),
    imgURL varchar(255)
);