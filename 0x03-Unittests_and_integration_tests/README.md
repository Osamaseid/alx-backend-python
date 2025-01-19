0x03-Unittests_and_integration_tests

4. Parameterize and patch as decorators
mandatory
Familiarize yourself with the client.GithubOrgClient class.

    """A Githib org client
    """
    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """Init method of GithubOrgClient"""
        self._org_name = org_name

    @memoize
    def org(self) -> Dict:
        """Memoize org"""
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """Public repos URL"""
        return self.org["repos_url"]

    @memoize
    def repos_payload(self) -> Dict:
        """Memoize repos payload"""
        return get_json(self._public_repos_url)

    def public_repos(self, license: str = None) -> List[str]:
        """Public repos"""
        json_payload = self.repos_payload
        public_repos = [
            repo["name"] for repo in json_payload
            if license is None or self.has_license(repo, license)
        ]

        return public_repos

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """Static: has_license"""
        assert license_key is not None, "license_key cannot be None"
        try:
            has_license = access_nested_map(repo, ("license", "key")) == license_key
        except KeyError:
            return False
        return has_license


In a new test_client.py file, declare the TestGithubOrgClient(unittest.TestCase) class and implement the test_org method.

This method should test that GithubOrgClient.org returns the correct value.

Use @patch as a decorator to make sure get_json is called once with the expected argument but make sure it is not executed.

Use @parameterized.expand as a decorator to parametrize the test with a couple of org examples to pass to GithubOrgClient, in this order:

google
abc
Of course, no external HTTP calls should be made.
 
5. Mocking a property
mandatory
memoize turns methods into properties. Read up on how to mock a property (see resource).

Implement the test_public_repos_url method to unit-test GithubOrgClient._public_repos_url.

Use patch as a context manager to patch GithubOrgClient.org and make it return a known payload.

Test that the result of _public_repos_url is the expected one based on the mocked payload.
 
6. More patching
mandatory
Implement TestGithubOrgClient.test_public_repos to unit-test GithubOrgClient.public_repos.

Use @patch as a decorator to mock get_json and make it return a payload of your choice.

Use patch as a context manager to mock GithubOrgClient._public_repos_url and return a value of your choice.

Test that the list of repos is what you expect from the chosen payload.

Test that the mocked property and the mocked get_json was called once.

 
7. Parameterize
mandatory
Implement TestGithubOrgClient.test_has_license to unit-test GithubOrgClient.has_license.

Parametrize the test with the following inputs

repo={"license": {"key": "my_license"}}, license_key="my_license"
repo={"license": {"key": "other_license"}}, license_key="my_license"
You should also parameterize the expected returned value.
 
8. Integration test: fixtures
mandatory
We want to test the GithubOrgClient.public_repos method in an integration test. That means that we will only mock code that sends external requests.

Create the TestIntegrationGithubOrgClient(unittest.TestCase) class and implement the setUpClass and tearDownClass which are part of the unittest.TestCase API.

Use @parameterized_class to decorate the class and parameterize it with fixtures found in fixtures.py. The file contains the following fixtures:

org_payload, repos_payload, expected_repos, apache2_repos
The setupClass should mock requests.get to return example payloads found in the fixtures.

Use patch to start a patcher named get_patcher, and use side_effect to make sure the mock of requests.get(url).json() returns the correct fixtures for the various values of url that you anticipate to receive.

Implement the tearDownClass class method to stop the patcher.
 
9. Integration tests
#advanced
Implement the test_public_repos method to test GithubOrgClient.public_repos.

Make sure that the method returns the expected results based on the fixtures.

Implement test_public_repos_with_license to test the public_repos with the argument license="apache-2.0" and make sure the result matches the expected value from the fixtures.

File: test_client.py

