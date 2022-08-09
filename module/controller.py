import re
import os.path
from re import Match
from typing import AnyStr
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import requests as requests
from requests import Response

from module.exception.scriptexception import ScriptException
from module.view import View


class Controller:

    def __init__(self):
        """
        Initialize a new instance of Controller class.
        """
        self.VIEW = View(100)
        self.URL_REPO = "https://repo1.maven.org/maven2/"

        self.USER: (str | None) = None
        self.GROUP: (str | None) = None
        self.VERSION: (str | None) = None
        self.ARTIFACT_ID: (str | None) = None

        self.PROXIES = {
            'http': 'http://proxy.intranet.cg59.fr:8080',
            'https': 'https://proxy.intranet.cg59.fr:8090',
        }

    def run(self, args: [str]):
        self.VIEW.title("FETCH ARTIFACT")
        try:
            self.VIEW.action("Check the script precondition")
            exit(-1) if not self.check_precondition(args) else self.VIEW.success()

            self.VIEW.action("Check the user data")
            self.__check_user__(args[2])
            self.VIEW.success()
            self.VIEW.info("The user is " + args[2], " ")

            self.VIEW.action("Extract artifact data")
            self.__extract_data__(args[1])
            self.VIEW.success()

            self.VIEW.info("Data extracted 'group' : " + self.GROUP, " ")
            self.VIEW.info("Data extracted 'artifact id' : " + self.ARTIFACT_ID, " ")
            self.VIEW.info("Data extracted 'version' : " + self.VERSION, " ")

            self.VIEW.action("Check the artifact and get the files list")
            file_list: [str] = self.__check_artifact_exists()
            self.VIEW.success()

            self.VIEW.title("Get the " + str(len(file_list) - 1) + " files of the artifact")
            for file in file_list:
                self.__get_file__(file)

            self.VIEW.info("Fetch all dependencies", " ")
            self.__fetch_dependencies__()

            exit(0)

        except ScriptException as e:
            self.VIEW.error(e.MESSAGE)
            exit(-1)

    def __fetch_dependencies__(self):
        pom_path: str = self.__get_artifact_path__() + "/" + self.ARTIFACT_ID + "-" + self.VERSION + ".pom"

        if not os.path.exists(pom_path):
            return

        root: Element = ElementTree.parse(pom_path).getroot()
        
        if re.match("\{[^}]+\}project", root.tag):
            xmlns: str = root.tag[0: root.tag.rindex("}") + 1]
        else:
            xmlns = ""

        for node in root.find(".//" + xmlns + "dependencies").findall(".//" + xmlns + "dependency"):

            group: str = node.find(".//" + xmlns + "groupId").text
            version: str = node.find(".//" + xmlns + "version").text
            artifact_id: str = node.find(".//" + xmlns + "artifactId").text

            self.VIEW.title("GROUP - " + group + " - FETCH ARTIFACT ID - " + artifact_id + " - " + version)

            Controller().run(["",
                              node.find(".//" + xmlns + "groupId").text + ":" +
                              node.find(".//" + xmlns + "artifactId").text + ":" +
                              node.find(".//" + xmlns + "version").text, self.USER]
                             )

    def __check_user__(self, username):
        if not os.path.exists("C:/Users/" + username):
            raise ScriptException("The user '" + username + "' do not exists ! ")
        self.USER = username

    def __get_artifact_url__(self):
        return self.URL_REPO + self.GROUP.replace(".", "/") + "/" + self.ARTIFACT_ID + "/" + self.VERSION

    def __get_artifact_path__(self):
        return "C:/Users/" + self.USER + "/.m2/repository/" + self.GROUP.replace(".", "/") + "/" + self.ARTIFACT_ID + \
               "/" + self.VERSION

    def __get_file__(self, file_link: str):
        """
        Get all the file og the artifact.;
        :param file_link: file name. ;
        """
        url: str = self.__get_artifact_url__() + "/" + file_link
        path: str = self.__get_artifact_path__()

        if not os.path.exists(path):
            self.VIEW.action("Create the folder " + self.GROUP.replace(".", "/") + "/" + self.ARTIFACT_ID +
                             "/" + self.VERSION)
            try:
                os.makedirs(path)
                self.VIEW.success()
            except Exception as e:
                self.VIEW.error("Error when create the folder '" + path + "'")
                print(e)
                return

        path_file: str = path + "/" + file_link

        response: Response = requests.get(url)
        content_type: str = response.headers.get("content-type")

        if not os.path.exists(path_file):

            self.VIEW.action("Creating file '" + file_link + "'")

            try:
                if content_type.__eq__("text/plain") or content_type.__eq__("text/xml"):
                    fd = open(path_file, "w")
                    fd.write(response.text)
                else:
                    fd = open(path_file, "wb")
                    fd.write(response.content)
                fd.close()

                self.VIEW.success()

            except Exception as e:
                self.VIEW.error("Error when create the file '" + file_link + "'")
                print(e)

    def __check_artifact_exists(self) -> [str]:
        """
        Check if the artifact exists. ;
        :return: The list of files to download.
        """
        url: str = self.__get_artifact_url__()
        response: (Response | None) = None

        # noinspection PyBroadException
        try:
            response = requests.get(url, self.PROXIES)
        except:
            if response is not None:
                raise ScriptException("The access to the artifact page '" + url + "' finish in " +
                                      str(response.status_code))
            else:
                raise ScriptException("An error occurs when trying to get '" + url + "'")

        result: [str] = []
        for line in response.text.split("\n"):
            matches: (None | Match[AnyStr]) = re.match("<a href=\"([^\"]+)\" title=\"([^\"]+)\">.*", line)
            if matches is not None:
                result.append(matches.groups()[0])

        return result

    def __extract_data__(self, dependency: str):
        """
        Extract data from the argument dependency.
        :param dependency: The argument dependency.
        """
        matches: ([AnyStr] | None) = re.match("([^:]+):([^:]+).([^:]+)", dependency)
        if matches is None or len(matches.groups()) != 3:
            raise ScriptException("The argument dependency is not well formed (group:artifact:version).")

        self.GROUP = matches.groups()[0]
        self.VERSION = matches.groups()[2]
        self.ARTIFACT_ID = matches.groups()[1]

    def check_precondition(self, args: [str]) -> bool:
        """
        Check the script preconditions. ;
        :param args: The script arguments. ;
        :return: False if the precondition are not respected; otherwise True.
        """
        if len(args) > 3:
            self.VIEW.error("The script only needs 2 arguments!")
            return False

        elif len(args) < 3:
            self.VIEW.error("The script needs 2 argument!")
            return False

        return True
