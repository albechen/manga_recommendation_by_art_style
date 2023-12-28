# Art-Driven Manga Recommendations

This project introduces a novel recommendation model using content-based filtering techniques with a unique focus on manga art style analysis through feature extraction with a pretrained image classifcation model. While most manga recommendation models primarily rely on collaborative filtering, this model prioritizes the exploration of manga art styles to enhance the recommendation process.

## Overview

The goals of this project was to create a recommendation system that will (1) implement an art style focused reccomendation (3) leverage ANIList tag and genre scores to support content based filtering

**Skill learned during project:**

1. Reccomenation **Content based filtering**
   - descriptors, genres, tags, and scores from MAL and ANIlist
2. Feature extraction with **pretrained image model**
   - familiarized myself with the image classificaiton world
   - applied **transfer learning** technique and feature extraction outputs
3. Description processing with **doc2vec** to process manga description to add to content based dataset
4. Data scrapping and API usage
   - have prior expereince in both, but it was good to practice again

## Data Sourcing and Scrapping

![manga_sites](/images/manga_sites.jpg "manga_sites")

There are three main data sources that were pulled from using either the offical API or a scrapping library. The goal was to have these final dataset:

1. Top 15k manga descriptors
   1. From MAL - descriptions, genres, published date, name, demographic
   2. From ANIlist - tags, genres, scores
2. Images of Chapter 1 - 5, pages 5-10 from mangadex

**Manga Descriptors**
MAL's API was used first to get a list of the top 15k manga on MAL and the associated descriptors with them (description, score, genre, demographic, date published). Luckily ANIlist also uses MAL manga id as a possible input to their API, so the tags, genres, and scores were pulled from ANIlist's API.

**Manga Images**
Manga images were scrapped from mangadex using a premade library to download managa from the site. First though google was scrapped for the right mangadex link to the manga and was cross check with the assocaited MAL id. Once all the correct managdex links was confrmed, manga pages were selectively downloaded from Chapter 1 - 5, pages 5-10 for each, along with the first cover image.

## Manga Content Based Filtering

SUMMARY

**Description Doc2Vec**
something

**Tags, Genres, and Demographic Data**
something

**Score and Popularity**
something

## Manga Art Style Feature Extraction

SUMMARY

**Processing and Cleaning Images for Model**
something

**Setting up XXX Model for Feature Extraction**
something

**Summarizing Feature Results per Manga**
something

## Analysis

## Conclusion

While the final product is by no means ready for any real applications, it was a great exercise in learning new skills. The project was mainly limited by (1) the accuracy of the cameras and the resulting location of my hand to flicker which caused stutters in the arm and (2) the lack of homing of the steppers. It would be interesting to pursue coding solutions to problem 1, but overall, I'm happy with the progress!

I greatly valued learning more about practical applications and integration of software with  physical products. It was a great jumping off point for more electrically or mechanically intensive projects I'm planning on in the future!

Also -- now I have an arm that can do this:
![final](/images/final_bread.gif "final_bread")
