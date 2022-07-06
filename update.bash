git pull
docker build -t by-quiz-bot-dbback .
docker run -d --name by-quiz-bot-dbback -p 7878:80 by-quiz-bot-dbback