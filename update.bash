ßgit pull
docker stop 5c619a5599ca
docker rm 5c619a5599ca
docker build -t by-quiz-bot-dbback .
docker run -d --name by-quiz-bot-dbback -p 7878:80 by-quiz-bot-dbback