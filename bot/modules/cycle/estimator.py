from rich import print
from rich.traceback import Traceback

from bot.utils.config import config

from ..providers.common.content import BasePhotos, BaseVideo
from ..providers.common.propagations import (
    PropagateAudioNeeded,
    PropagateEverythingNeeded,
    PropagatePhotosNeeded,
    PropagateVideoNeeded,
)
from .cycle import LinkCycle
from ..providers import NoProvidersLeft


def __process_estimated(cycle: LinkCycle):
    estimated = cycle.estimated
    if isinstance(estimated, BaseVideo):
        cycle.video = estimated
        cycle.job.set_send()
        return cycle

    elif isinstance(estimated, BasePhotos):
        cycle.photos = estimated
        if estimated.audio_url:
            cycle.audio = estimated.audio_url
        cycle.job.set_send()

    elif any(
        isinstance(estimated, x)
        for x in [
            PropagateAudioNeeded,
            PropagateEverythingNeeded,
            PropagatePhotosNeeded,
            PropagateVideoNeeded,
        ]
    ):
        for x in cycle.can_propagate:
            setattr(cycle, x, getattr(estimated, x)) if hasattr(
                estimated, x
            ) and getattr(estimated, x) else ...
        cycle.needs = estimated
        cycle.job.set_estimate()

    cycle.estimated = None
    return cycle


async def process_situation(cycle: LinkCycle) -> LinkCycle:
    try:
        if cycle.job.estimate and not cycle.needs:
            cycle.estimated = await cycle.providers.get_next().from_url(cycle.url)
            return __process_estimated(cycle)

        elif cycle.job.estimate and cycle.needs:
            provider = cycle.providers.get_for_type(cycle.needs.needs)
            cycle.estimated = await (
                provider.from_preferred(getattr(cycle, provider.wants))
                if getattr(cycle, provider.wants)
                else provider.from_url(cycle.url)
            )
            return __process_estimated(cycle)

        elif cycle.photos or cycle.video:
            cycle.job.set_send()
            return cycle

    except NoProvidersLeft:
        cycle.set_error()
        return cycle

    except Exception as e:
        assert e
        if config.log.log_cycle_errors:
            print("ERROR IN CYCLE")
            print(Traceback(show_locals=True))
            print("END ERROR IN CYCLE")
        return cycle
