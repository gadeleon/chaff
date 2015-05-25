***

# WITH GREAT POWER COMES GREAT RESPONSIBILITY

***


# ABOUT CHAFF


Chaff is an anti-phishing command line tool written in Python. In nature, Chaff is the protective coating on cereal grain that protects it from all sort of unwanted attention. The military adopted the phrase to describe their countermeasures for radar-guided missiles. Chaff.py is a similar concept: the tool itself can generate phony account credentials that it then stuffs into phishing forms. This can be used to flood a phisher's site and, if enough data is sent, cause them to go over data limits on certain popular free sites which limits the amount of valid accounts appearing. By default, Chaff will only use the @example.com email address; however, if you are a Google Apps domain, you can register Chaff with the directory API & generate credentials, verify against your domain, and send out the fake/invalid ones.

Chaff is capable of basic HTML parsing and can try and find find the fields, method, action url of phishing websites but the most reliable option is to inspect the sites yourselves and manually plug them into the configuration file. 

By design Chaff will only send invalid email accounts to phishing and can verify with Google's directory API if the email address/account it makes is fake. This may be more advantageous since @example.com can be filtered out relatively easily should an attacker want to review their logs for hits. It currently only supports Google so if people want to have it check against other systems, make a pull request!


## REQUIREMENTS


Python 2.7

Python SetupTools ( `sudo apt-get install python-pip` )

The Following libraries will be installed when running the setup script:
* beautifulsoup4
* requests
* google-api-python-client



## INSTALLATION 

1. Download the latest version
2. From terminal, run setup.py -- `sudo python setup.py install`; a config file named 'chaff_config' will be created upon successful installation. 
3. Update chaff_config with the full path of the 1000.json file included.


## About 1000.json

1000.json is where Chaff gets it random user data. The kind developers over at randomuser.me provided me with a local file when I expressed a desire to create large amount of users in a short amount of time. Chaff will use 1000.json to generate a fake account by randomly picking from the appropriate field out of the entire 1000 entries. This gives a decent amount of entropy to the users Chaff creates. If for whatever reason you need your own unique json file to create random users with, you can generate a file of up to 20 entries via api.randomuser.me and Chaff should use it sans issue (unless their format has changed since development).

## Quick Start

1. (Optional) Register Chaff with your google apps domain & create a token allowing you to authenticate against your email domain and ensure you only send invalid accounts.  
2. Specify the as much detail as needed from the phishing form in the chaff_config file. Inspect the website to get the action url, method, form's id's value on the site.
3. (Optional) Run `chaff.py --parse-form` and Chaff will try and parse the URL for the form and it's relevant IDs, method, etc. Not 100% guaranteed to work!
4. Update chaff_config with the most appropriate values from the phishing form (eg: Full Name = id_g3892392 on the phishing site, method, action url)
5. Run chaff.py, you can specifiy --entries and --delay so you can pace your form stuffing. 


## Using Chaff With Your Google Apps Domain

Chaff uses the Google's **directory api** in order to verify if accounts are fake before sending the data. When registering Chaff, I highly reccomend you limit access to the directory api as **read-only**. You can then create and store a token for repeated use. Add the token's full path & your domain to the config file and it will check if email addresses are invalid before submitting the data to the account. Google provides documentation on how to go about creating a token here: https://developers.google.com/admin-sdk/directory/v1/quickstart/quickstart-python NOTE: You will want to add a line or two storing the token!

Once you have the token, you can specify it's location in the config file **including** the **full working directory**. Chaff will take care of the rest.

## Making Additional Configuration Files

Instead of having to revise the same configuration file for different websites, launching `chaff_configure.py --new-config NAME` will make a new configure script with the name `NAME`. When you want to send chaff to a site and not use the default *chaff_config* file, use `python chaff.py --config CONFIG_FILE` and it will load the specificed config file instead.  


## Example Usage

Have Chaff try and parse the URL in your default config file

```bash
python chaff.py --parse-form
```

Send chaff to the URL/form in your default config file 10 times over 1 minute

```bash
python chaff.py --entries 10 --delay 6.0
```

Send chaff to a form 1000 times over 1 minute with a different config file

```bash
python chaff.py --entries 1000 --delay 0.06 --config secondary_config
```

## Known Issues

* While doing my best, I'm confident I have not made this software bug free and I'm sure there's plenty of unintended uses that I'm unaware of. That doesn't mean I won't fix them, I just need to be told they exist.
* If you register with Google Apps and enter an incorrect email domain, Chaff will look for the incorrect email address it generates and naturally say it's okay. johhny_important@domain.site would not like if chaff inputs johhny_important@domain.sit, especially for spear-phishing campaigns where the attacker can assume at typo.
* Chaff does not currently make use of entry points. Since the config file uses full paths for the auth token & json file, it probably should.
* This is a highly offensive tool. Please use responsibly and safely.
