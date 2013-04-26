## About
Scalability Testing Tool for Katello systems.

## Requirements
* Install **Gradle** from http://gradle.org. Optionally, download and extract the latest release (zip file) and make sure to include it in your system's path.

## Assumptions

* You already have a system with either katello or headpin installed and configured
* You have an **automation.properties** configured to access said system
* You have a different system where you can call the katello API
 * It is also assumed that you have gradle installed
* The default user who is used for the automation **must** have a default organization and environment set
* The organization must have a valid Red Hat manifest file imported and repositories have been synced and promoted to a valid environment

## Configuration
Copy *automation.properties.sample* to your $HOME directory and rename it to *automation.properties*:

  `$ cp automation.properties.sample automation.properties`

Alternatively, you may tell grinder where your properties file is located:

  `$ gradle -Dautomation.propertiesfile=<PATH_TO_PROPERTIES_FILE>`

Open a separate console and start the gradle console:

  `$ gradle console`

The first time you start the console you will see all dependencies listed in *build.gradle* downloaded and compiled. If everything goes well, you should see the a new gradle UI console.

Now, open another separate console and start the gradle worker:

  `$gradle exec`

The gradle UI console should now have some extra features added to the UI and a new **Play** button should be visible and enabled.

## Running
Once you have a gradle console and worker running, click the **Play** button in the console UI to run the system registration tests. By default only one system will be created during this test.

To change the number of systems that will be created, simply modify the following property in the  *grinder.properties* file:

    grinder.runs=1

It is also possible to change the number of simultaneous systems that get created by changing the number of threads to use. Just modify the following property:

    grinder.threads=1

As an example the following configuration would create a total of 128 new systems, 2 systems at a time:

    grinder.runs=64
    grinder.threads=2

## Advanced uses
You can pre-populate your environment with multiple clients prior to running a test (useful if you want to see how your system will behave already under a certain load) by running the following useful script:

    gradle populate -Dkatello.initialSystems=100 -Dkatello.organization=ACME_Corporation