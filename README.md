# miner_weekly_report
Calculate GPUMine payment weekly and display on web page.

## How to
1. Edit miner.ini
    ```
    [miner]
    miner1=0x123456777....
    miner2=0xABCDEFGHI.... 
    ```

2. Make payments.py as a service
3. Restart service every week (crontab)
    ``` 
    0 17 * * sat sudo /bin/systemctl restart your_app.service
    ```

