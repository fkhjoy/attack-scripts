try:
    from ..core.filter import Filter, Filterv4
    from ..core.layout import Layout
    from ..core.technique import Technique
    from ..core.gradient import Gradient
    from ..core.legenditem import LegendItem
    from ..core.metadata import Metadata
    from ..core.exceptions import UNSETVALUE, typeChecker, BadInput, handler, \
        categoryChecker, UnknownLayerProperty
except ValueError:
    from core.filter import Filter
    from core.layout import Layout
    from core.technique import Technique
    from core.gradient import Gradient
    from core.legenditem import LegendItem
    from core.metadata import Metadata
    from core.exceptions import UNSETVALUE, typeChecker, BadInput, handler, \
        categoryChecker, UnknownLayerProperty

class _LayerObj:
    def __init__(self, version, name, domain):
        """
            Initialization - Creates a layer object

            :param version: The corresponding att&ck layer version
            :param name: The name for this layer
            :param domain: The domain for this layer (mitre-enterprise
                or mitre-mobile)
        """
        self.version = version
        self.name = name
        self.__description = UNSETVALUE
        self.domain = domain
        self.__filters = UNSETVALUE
        self.__sorting = UNSETVALUE
        self.__layout = UNSETVALUE
        self.__hideDisabled = UNSETVALUE
        self.__techniques = UNSETVALUE
        self.__gradient = UNSETVALUE
        self.__legendItems = UNSETVALUE
        self.__showTacticRowBackground = UNSETVALUE
        self.__tacticRowBackground = UNSETVALUE
        self.__selectTechniquesAcrossTactics = UNSETVALUE
        self.__selectSubtechniquesWithParent = UNSETVALUE
        self.__metadata = UNSETVALUE

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version):
        typeChecker(type(self).__name__, version, str, "version")
        categoryChecker(type(self).__name__, version, ["3.0", "4.0"], "version")
        self.__version = version

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        typeChecker(type(self).__name__, name, str, "name")
        self.__name = name

    @property
    def domain(self):
        return self.__domain

    @domain.setter
    def domain(self, domain):
        typeChecker(type(self).__name__, domain, str, "domain")
        categoryChecker(type(self).__name__, domain, ["mitre-enterprise",
                                                      "mitre-mobile"],
                        "domain")
        self.__domain = domain

    @property
    def description(self):
        if self.__description != UNSETVALUE:
            return self.__description

    @description.setter
    def description(self, description):
        typeChecker(type(self).__name__, description, str, "description")
        self.__description = description

    @property
    def filters(self):
        if self.__filters != UNSETVALUE:
            return self.__filters

    @filters.setter
    def filters(self, filters):
        if self.version == "4.0":
            temp = Filterv4(self.domain)
        else:
            temp = Filter(self.domain)
        try:
            if self.version != "4.0":
                temp.stages = filters['stages']
            temp.platforms = filters['platforms']
            self.__filters = temp
        except KeyError as e:
            handler(type(self).__name__, "Unable to properly extract "
                                         "information from filter: {}."
                    .format(e))
            raise BadInput

    @property
    def sorting(self):
        if self.__sorting != UNSETVALUE:
            return self.__sorting

    @sorting.setter
    def sorting(self, sorting):
        typeChecker(type(self).__name__, sorting, int, "sorting")
        categoryChecker(type(self).__name__, sorting, [0, 1, 2, 3], "sorting")
        self.__sorting = sorting

    @property
    def layout(self):
        if self.__layout != UNSETVALUE:
            return self.__layout

    @layout.setter
    def layout(self, layout):
        temp = Layout()
        if "layout" in layout:
            temp.layout = layout['layout']
        if "showName" in layout:
            temp.showName = layout['showName']
        if "showID" in layout:
            temp.showID = layout['showID']
        self.__layout = temp

    @property
    def hideDisabled(self):
        if self.__hideDisabled != UNSETVALUE:
            return self.__hideDisabled

    @hideDisabled.setter
    def hideDisabled(self, hideDisabled):
        typeChecker(type(self).__name__, hideDisabled, bool, "hideDisabled")
        self.__hideDisabled = hideDisabled

    @property
    def techniques(self):
        if self.__techniques != UNSETVALUE:
            return self.__techniques

    @techniques.setter
    def techniques(self, techniques):
        typeChecker(type(self).__name__, techniques, list, "techniques")
        self.__techniques = []
        entry = ""
        try:
            for entry in techniques:
                temp = Technique(entry['techniqueID'])
                temp._loader(entry)
                self.__techniques.append(temp)
        except KeyError as e:
            handler(type(self).__name__, "Unable to properly extract "
                                         "information from technique {}: {}."
                    .format(entry, e))
            raise BadInput

    @property
    def gradient(self):
        if self.__gradient != UNSETVALUE:
            return self.__gradient

    @gradient.setter
    def gradient(self, gradient):
        try:
            self.__gradient = Gradient(gradient['colors'],
                                       gradient['minValue'],
                                       gradient['maxValue'])
        except KeyError as e:
            handler(type(self).__name__, 'Gradient is missing parameters: {}. '
                                         'Unable to load.'.format(e))

    @property
    def legendItems(self):
        if self.__legendItems != UNSETVALUE:
            return self.__legendItems

    @legendItems.setter
    def legendItems(self, legendItems):
        typeChecker(type(self).__name__, legendItems, list, "legendItems")
        self.__legendItems = []
        entry = ""
        try:
            for entry in legendItems:
                temp = LegendItem(entry['label'], entry['color'])
                self.__legendItems.append(temp)
        except KeyError as e:
            handler(type(self).__name__, 'LegendItem {} is missing parameters:'
                                         ' {}. Unable to load.'
                    .format(entry, e))

    @property
    def showTacticRowBackground(self):
        if self.__showTacticRowBackground != UNSETVALUE:
            return self.__showTacticRowBackground

    @showTacticRowBackground.setter
    def showTacticRowBackground(self, showTacticRowBackground):
        typeChecker(type(self).__name__, showTacticRowBackground, bool,
                    "showTacticRowBackground")
        self.__showTacticRowBackground = showTacticRowBackground

    @property
    def tacticRowBackground(self):
        if self.__tacticRowBackground != UNSETVALUE:
            return self.__tacticRowBackground

    @tacticRowBackground.setter
    def tacticRowBackground(self, tacticRowBackground):
        typeChecker(type(self).__name__, tacticRowBackground, str,
                    "tacticRowBackground")
        self.__tacticRowBackground = tacticRowBackground

    @property
    def selectTechniquesAcrossTactics(self):
        if self.__selectTechniquesAcrossTactics != UNSETVALUE:
            return self.__selectTechniquesAcrossTactics

    @selectTechniquesAcrossTactics.setter
    def selectTechniquesAcrossTactics(self, selectTechniquesAcrossTactics):
        typeChecker(type(self).__name__, selectTechniquesAcrossTactics, bool,
                    "selectTechniqueAcrossTactics")
        self.__selectTechniquesAcrossTactics = selectTechniquesAcrossTactics

    @property
    def selectSubtechniquesWithParent(self):
        if self.__selectSubtechniquesWithParent != UNSETVALUE:
            return self.__selectSubtechniquesWithParent

    @selectSubtechniquesWithParent.setter
    def selectSubtechniquesWithParent(self, selectSubtechniquesWithParent):
        typeChecker(type(self).__name__, selectSubtechniquesWithParent, bool,
                    "selectSubtechniquesWithParent")
        self.__selectSubtechniquesWithParent = selectSubtechniquesWithParent

    @property
    def metadata(self):
        if self.__metadata != UNSETVALUE:
            return self.__metadata

    @metadata.setter
    def metadata(self, metadata):
        typeChecker(type(self).__name__, metadata, list, "metadata")
        self.__metadata = []
        entry = ""
        try:
            for entry in metadata:
                self.__metadata.append(Metadata(entry['name'], entry['value']))
        except KeyError as e:
            handler(type(self).__name__, 'Metadata {} is missing parameters: '
                                         '{}. Unable to load.'
                    .format(entry, e))

    def _enumerate(self):
        """
            INTERNAL: Identifies which fields have been set for this Layer
                object
            :returns: a list of all set fields within this Layer object
        """
        temp = ['name', 'version', 'domain']
        if self.description:
            temp.append('description')
        if self.filters:
            temp.append('filters')
        if self.sorting:
            temp.append('sorting')
        if self.layout:
            temp.append('layout')
        if self.hideDisabled:
            temp.append('hideDisabled')
        if self.techniques:
            temp.append('techniques')
        if self.gradient:
            temp.append('gradient')
        if self.legendItems:
            temp.append('legendItems')
        if self.showTacticRowBackground:
            temp.append('showTacticRowBackground')
        if self.tacticRowBackground:
            temp.append('tacticRowBackground')
        if self.selectTechniquesAcrossTactics:
            temp.append('selectTechniquesAcrossTactics')
        if self.selectSubtechniquesWithParent:
            temp.append('selectSubtechniquesWithParent')
        if self.metadata:
            temp.append('metadata')
        return temp

    def get_dict(self):
        """
            Converts the currently loaded layer into a dict
            :returns: A dict representation of the current layer object
        """
        temp = dict(name=self.name, version=self.version, domain=self.domain)

        if self.description:
            temp['description'] = self.description
        if self.filters:
            temp['filters'] = self.filters.get_dict()
        if self.sorting:
            temp['sorting'] = self.sorting
        if self.layout:
            temp['layout'] = self.layout.get_dict()
        if self.hideDisabled is not None:
            temp['hideDisabled'] = self.hideDisabled
        if self.techniques:
            temp['techniques'] = [x.get_dict() for x in self.techniques]
        if self.gradient:
            temp['gradient'] = self.gradient.get_dict()
        if self.legendItems:
            temp['legendItems'] = [x.get_dict() for x in self.legendItems]
        if self.showTacticRowBackground is not None:
            temp['showTacticRowBackground'] = self.showTacticRowBackground
        if self.tacticRowBackground:
            temp['tacticRowBackground'] = self.tacticRowBackground
        if self.selectTechniquesAcrossTactics is not None:
            temp['selectTechniquesAcrossTactics'] = \
                self.selectTechniquesAcrossTactics
        if self.selectSubtechniquesWithParent is not None:
            temp['selectSubtechniquesWithParent'] = \
                self.selectSubtechniquesWithParent
        if self.metadata:
            temp['metadata'] = [x.get_dict() for x in self.metadata]
        return temp

    def _linker(self, field, data):
        """
            INTERNAL: Acts as a middleman routing the settings of values
                within the layer
            :param field: The value field being set
            :param data: The corresponding data to set that field to
            :raises UnknownLayerProperty: An error indicating that an
                unexpected property was identified
        """
        if field == 'description':
            self.description = data
        elif field == 'filters':
            self.filters = data
        elif field == 'sorting':
            self.sorting = data
        elif field == 'layout':
            self.layout = data
        elif field == 'hideDisabled':
            self.hideDisabled = data
        elif field == 'techniques':
            self.techniques = data
        elif field == 'gradient':
            self.gradient = data
        elif field == 'legendItems':
            self.legendItems = data
        elif field == 'showTacticRowBackground':
            self.showTacticRowBackground = data
        elif field == 'tacticRowBackground':
            self.tacticRowBackground = data
        elif field == 'selectTechniquesAcrossTactics':
            self.selectTechniquesAcrossTactics = data
        elif field == 'selectSubtechniquesWithParent':
            self.selectSubtechniquesWithParent = data
        elif field == 'metadata':
            self.metadata = data
        else:
            handler(type(self).__name__, "Unknown layer property: {}"
                    .format(field))
            raise UnknownLayerProperty
