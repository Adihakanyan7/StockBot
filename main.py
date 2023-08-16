from server import updater

def main():
    print("Starting bot...")
    try:
        updater.start_polling()
        print("Bot polling started...")
        updater.idle()
    except Exception as e:
        print(f"Error: {e}")
    print("Bot stopped.")

if __name__ == "__main__":
    main()
