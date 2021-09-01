FROM golang:alpine

WORKDIR /go/src/app

COPY . .

RUN go build main.go

EXPOSE 6111

CMD ["./main"]