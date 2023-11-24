from autofw.ui_base.ui_element_handler import UIElementHandler
from autofw.utilities.logger import logger

class UILink(UIElementHandler):
    def go_to_link(self, input_link):
        """It will open the link which is inputted.

        Parameters
        ----------
        input_link: str
            The input_link is the link to be open

        Returns
        -------
        bool value
        """
        try:
            self.driver.get(input_link)
            logger.info("go_to_link method open link which is inputted")
            return True
        except:
            logger.error(
                "go_to_link method can't able to open link which is inputted"
            )
            return False