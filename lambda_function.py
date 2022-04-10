from main import main


def lambda_handler(event, context):
    
    main()
    print("update complete")