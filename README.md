# WoW Forever Addons

Index of the TIMID-Group addons for WoW Forever (interface 16001). Each addon is its own private
repo; access is per repo.

| Addon | Description | Optional deps |
| --- | --- | --- |
| [ForeverCraftingLedger](https://github.com/TIMID-Group/ForeverCraftingLedger) ([latest](https://github.com/TIMID-Group/ForeverCraftingLedger/releases/latest)) | What every recipe of every profession earns: each material from your cheapest vendor or the auction house, the product sold to a vendor or auctioned. Named shopping lists with your own prices. Reads Auctionator's prices. | ForeverCookingLedger, Auctionator, AtlasLootClassic, QuestieDB, TomTom |
| [ForeverFishingChart](https://github.com/TIMID-Group/ForeverFishingChart) ([latest](https://github.com/TIMID-Group/ForeverFishingChart/releases/latest)) | Fishing waters on the world map: catches, skill checks and time-of-day rates, plus a fish finder and your own catch log. | TomTom |
| [[classified]](https://github.com/TIMID-Group/[classified]) ([latest](https://github.com/TIMID-Group/[classified]/releases/latest)) | Hold a price ceiling on the auction house. Posts your wall when nothing is listed at or below your price, buys what undercuts it, and tracks every session's profit and gold per hour. | ForeverCraftingLedger, ForeverCookingLedger, Auctionator |
| [ForeverQuestLeftovers](https://github.com/TIMID-Group/ForeverQuestLeftovers) ([latest](https://github.com/TIMID-Group/ForeverQuestLeftovers/releases/latest)) | Looks through your bags and bank for items no quest needs any more, says why, and says what to do with each one. It only advises. It never sells or destroys anything. | Questie, QuestieDB |
| [ForeverWorkbench](https://github.com/TIMID-Group/ForeverWorkbench) ([latest](https://github.com/TIMID-Group/ForeverWorkbench/releases/latest)) | Makes the profession window richer. Shows materials on hand and items in bags on every recipe, buys the vendor materials for a recipe while leaving bag space to craft, and sells what you crafted. | ForeverCraftingLedger, ForeverCookingLedger, [classified], [classified] |

## Install

Download the `<Addon>-X.Y.Z.zip` asset from the addon's latest release (not the source archive)
and extract it into `World of Warcraft/_forever_/Interface/AddOns/`, giving
`AddOns/<Addon>/<Addon>.toc`. To update, replace the folder. Saved settings live in `WTF/` and
are not touched.

Watch a repo with **Custom > Releases** to be notified of new versions.

## Versioning

Tags are `vX.Y.Z` and match `## Version` in the addon's `.toc`. Every tag has a GitHub release
with the installable zip attached.

## Issues

File them on the addon's own repo.
