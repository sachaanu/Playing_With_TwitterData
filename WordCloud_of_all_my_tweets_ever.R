library(tm)
library(SnowballC)
library(wordcloud)

tweets <- read.csv('tweets.csv')
head(tweets)

head(tweets['text'])

tweet_text <- tweets['text']

tweets_text <- tweet_text[!(tweet_text$text ==""),]
tweets2 <- gsub('[0-9]+', '', tweets_text)

tweet_text_Corpus <- Corpus(VectorSource(tweets2))

Corpus <- tm_map(tweet_text_Corpus, removePunctuation)

Corpus_2 <- tm_map(Corpus, removeWords, c("the", "this", stopwords('english')))
print(Corpus_2)
Corpus_3 <- tm_map(Corpus_2, stemDocument)

head(Corpus_2)
dtm <- TermDocumentMatrix(Corpus_3)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
head(d, 10)

library('RColorBrewer')
par(bg='grey30')
png(file="WordCloud_of_my_Tweets.png",width=1000,height=700, bg="grey30")
wordcloud(d$word, d$freq, col=terrain.colors(length(d$word), alpha=0.9), random.order=FALSE, rot.per=0.3 )
title(main = "Word_Cloud_Of_All_My_Tweets_Ever", font.main = 1, col.main = "cornsilk3", cex.main = 1.5)
dev.off()
