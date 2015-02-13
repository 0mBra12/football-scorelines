# Stats about european football

from api.match_utils import MatchUtils

englishFolderList = ["../../dataset/actual/England/PL-2013-2014",
                      "../../dataset/actual/England/PL-2012-2013",
                      "../../dataset/actual/England/PL-2011-2012",
                      "../../dataset/actual/England/PL-2010-2011",
                      "../../dataset/actual/England/PL-2009-2010",
                      "../../dataset/actual/England/PL-2008-2009",
                      "../../dataset/actual/England/PL-2007-2008"]

englishMatchList = MatchUtils.findMatchListInFolders(englishFolderList)

