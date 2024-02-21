library(ggplot2)
library(jsonlite)

historical_data <- fromJSON(file.choose())
trades_table <- historical_data$data$tradesTable$rows

framed_historical_data <- as.data.frame(trades_table)

framed_historical_data <-
    as.data.frame(
        lapply(
            framed_historical_data,
            gsub,
            pattern = "$",
            fixed = TRUE,
            replacement = ""
        )
    )

colnames(framed_historical_data) <-
  c("Date", "Close", "Volume", "Open", "High", "Low")
framed_historical_data$Close <- as.numeric(framed_historical_data$Close)
framed_historical_data$Open <- as.numeric(framed_historical_data$Open)
framed_historical_data$High <- as.numeric(framed_historical_data$High)
framed_historical_data$Low <- as.numeric(framed_historical_data$Low)
write.csv(framed_historical_data, "historical_data.csv")

plot(framed_historical_data$Close, xlab = "Date", ylab = "Closing Price")
lines(framed_historical_data$Close)

ggplot(data = framed_historical_data, aes(x = Date, y = Close)) +
    geom_point(stat = "identity") +
    geom_line(stat = "identity", color = "red") +
    scale_x_continuous(breaks = framed_historical_data$Date)
