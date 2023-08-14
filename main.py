from server import updater


def main():
    print("Starting bot...")
    updater.start_polling()
    updater.idle()
    print("Bot stopped.")


if __name__ == "__main__":
    main()
